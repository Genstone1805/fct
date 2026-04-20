import json
from datetime import date, time
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from routes.models import Route
from .emails import send_reservation_to_passenger
from .models import Booking, PassengerDetail, TransferInformation


@override_settings(API_KEY="test-api-key", EMAIL_FROM="admin@example.com")
class BookingAdminEmailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.api_key_headers = {"HTTP_API_KEY": "test-api-key"}
        self.route = Route.objects.create(
            from_location="Vienna Airport",
            to_location="Salzburg",
            meta_title="Vienna Airport to Salzburg",
            meta_description="Route meta description",
            hero_title="Vienna Airport to Salzburg Transfer",
            sub_headline="Comfortable ride",
            cash_deposit_percent=20,
            body="Route body",
            distance="300 km",
            time="3 hours",
            duration_minutes=180,
            sedan_price=150,
            van_price=220,
            what_makes_better=[],
            whats_included=[],
            reminder=[],
            cross_border_information=[],
            destination_highlights=[],
            ideal_for=[],
            image="routes/test.jpg",
            book_cta_label="Book now",
            book_cta_support="Support text",
        )

    @patch("booking.views.send_reservation_to_passenger")
    @patch("booking.admin_emails._send_html_email")
    def test_booking_create_admin_email_contains_booking_details(
        self,
        mock_send_html_email,
        mock_send_reservation_to_passenger,
    ):
        response = self.client.post(
            reverse("booking-create"),
            {
                "route": self.route.route_id,
                "amount_paid": "50.00",
                "outstanding_amount": "100.00",
                "total_amount": "150",
                "vehicle_type": "sedan",
                "payment_type": "card",
                "transaction_id": "txn_12345",
                "trip_type": "One Way",
                "pickup_date": "2026-05-01",
                "pickup_time": "10:30:00",
                "time_period": "Day Tariff",
                "transfer_information": json.dumps(
                    {
                        "flight_number": "OS101",
                        "adults": 2,
                        "children": 1,
                        "luggage": "Large",
                    }
                ),
                "passenger_information": json.dumps(
                    {
                        "full_name": "Jane Doe",
                        "phone_number": "+1234567890",
                        "email_address": "jane@example.com",
                        "additional_information": "Need a child seat",
                    }
                ),
            },
            **self.api_key_headers,
        )

        self.assertEqual(response.status_code, 201)
        mock_send_reservation_to_passenger.assert_called_once()
        mock_send_html_email.assert_called_once()

        booking = Booking.objects.get(passenger_information__email_address="jane@example.com")
        subject, greeting, message, detail, recipient = mock_send_html_email.call_args.args

        self.assertEqual(subject, "New Reservation Submitted – Action Required")
        self.assertEqual(greeting, "Hello Admin")
        self.assertEqual(recipient, "admin@example.com")
        self.assertIn(booking.booking_id, detail)
        self.assertIn("Vienna Airport", detail)
        self.assertIn("Salzburg", detail)
        self.assertIn("Jane Doe", detail)
        self.assertIn("jane@example.com", detail)
        self.assertIn("+1234567890", detail)
        self.assertIn("OS101", detail)
        self.assertIn("Need a child seat", detail)
        self.assertIn("card", detail)
        self.assertIn("pending", detail)
        self.assertIn("50.00", detail)
        self.assertIn("100.00", detail)
        self.assertIn("150.00", detail)

    @patch("booking.views.send_reservation_to_passenger")
    @patch("booking.admin_emails._send_html_email")
    def test_booking_create_accepts_bracket_notation_and_preserves_notes(
        self,
        mock_send_html_email,
        mock_send_reservation_to_passenger,
    ):
        response = self.client.post(
            reverse("booking-create"),
            {
                "route": self.route.route_id,
                "amountPaid": "80.00",
                "outstandingAmount": "70.00",
                "totalAmount": "150",
                "vehicleType": "sedan",
                "paymentType": "card",
                "transactionId": "txn_67890",
                "tripType": "One Way",
                "pickupDate": "2026-05-02",
                "pickupTime": "11:45:00",
                "timePeriod": "Day Tariff",
                "transferInformation[flightNumber]": "OS202",
                "transferInformation[adults]": "3",
                "transferInformation[children]": "1",
                "transferInformation[luggage]": "Large",
                "passengerInformation[fullName]": "Alex Smith",
                "passengerInformation[phoneNumber]": "+1987654321",
                "passengerInformation[emailAddress]": "alex@example.com",
                "passengerInformation[additionalInformation]": "Need a booster seat",
            },
            **self.api_key_headers,
        )

        self.assertEqual(response.status_code, 201)
        mock_send_reservation_to_passenger.assert_called_once()
        mock_send_html_email.assert_called_once()

        booking = Booking.objects.get(passenger_information__email_address="alex@example.com")
        self.assertEqual(booking.transfer_information.adults, 3)
        self.assertEqual(booking.transfer_information.children, 1)
        self.assertEqual(
            booking.passenger_information.additional_information,
            "Need a booster seat",
        )

        _, _, _, detail, _ = mock_send_html_email.call_args.args
        self.assertIn("Adults:</strong> 3", detail)
        self.assertIn("Children:</strong> 1", detail)
        self.assertIn("Need a booster seat", detail)

    @patch("booking.emails._send_html_email")
    def test_reservation_email_does_not_request_details_again(self, mock_send_html_email):
        transfer_info = TransferInformation.objects.create(
            flight_number="OS303",
            adults=2,
            children=0,
            luggage="Large",
        )
        passenger_info = PassengerDetail.objects.create(
            full_name="Chris Doe",
            phone_number="+1122334455",
            email_address="chris@example.com",
            additional_information="Please allow extra luggage space",
        )
        booking = Booking.objects.create(
            route=self.route,
            amount_paid=55,
            outstanding_amount=95,
            total_amount=150,
            vehicle_type="sedan",
            payment_type="card",
            transaction_id="txn_mail_1",
            trip_type="One Way",
            pickup_date=date(2026, 5, 3),
            pickup_time=time(9, 15),
            time_period="Day Tariff",
            transfer_information=transfer_info,
            passenger_information=passenger_info,
        )

        sent = send_reservation_to_passenger(booking)

        self.assertTrue(sent)
        subject, greeting, message, detail, recipient = mock_send_html_email.call_args.args
        self.assertEqual(subject, "New Booking Reservation (Pending Order)")
        self.assertEqual(greeting, "Hello Chris Doe")
        self.assertEqual(recipient, "chris@example.com")
        self.assertIn("reviewing the details of your reservation", message)
        self.assertIn("assign your driver", message)
        self.assertNotIn("provide us with the exact pickup address", message)
        self.assertNotIn("feel free to let us know", message)
        self.assertIn(booking.booking_id, detail)
