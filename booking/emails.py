from django.core.mail import send_mail
from django.conf import settings
from contextlib import suppress


def send_driver_assigned_to_passenger(booking):
    """
    Send email to passenger notifying them that a driver has been assigned to their booking.
    """
    passenger = booking.passenger_information
    driver = booking.driver
    route = booking.route

    if not passenger or not passenger.email_address or not driver:
        return False

    subject = f"Driver Assigned to Your Booking #{booking.booking_id}"

    message = f"""
Dear {passenger.full_name},

Great news! A driver has been assigned to your booking.

Booking Details:
- Booking ID: {booking.booking_id}
- Route: {route.from_location} → {route.to_location}
- Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
- Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}

Driver Information:
- Name: {driver.full_name}
- Phone: {driver.phone_number or 'Will be provided'}

{"Return Trip Details:" if booking.trip_type == "Return" else ""}
{f"- Return Date: {booking.return_date.strftime('%B %d, %Y')}" if booking.return_date else ""}
{f"- Return Time: {booking.return_time.strftime('%I:%M %p')}" if booking.return_time else ""}

Your driver will be at the pickup location on time. Please ensure you are ready at the scheduled time.

If you have any questions, please don't hesitate to contact us.

Best regards,
First Class Transfer Team
    """.strip()

    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [passenger.email_address],
            fail_silently=False,
        )
        return True

    return False


def send_booking_assigned_to_driver(booking):
    """
    Send email to driver notifying them that they have been assigned to a booking.
    """
    driver = booking.driver
    passenger = booking.passenger_information
    route = booking.route
    vehicle = booking.vehicle

    if not driver or not driver.email:
        return False

    subject = f"New Booking Assignment - #{booking.booking_id}"

    dashboard_url = f"{settings.FRONTEND_URL}/driver/bookings"

    vehicle_info = ""
    if vehicle:
        vehicle_info = f"""
Vehicle Assigned:
- {vehicle.make} {vehicle.model}
- License Plate: {vehicle.license_plate}
- Type: {vehicle.type}
"""

    message = f"""
Dear {driver.full_name},

You have been assigned to a new booking.

Booking Details:
- Booking ID: {booking.booking_id}
- Route: {route.from_location} → {route.to_location}
- Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
- Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
- Estimated Duration: {route.duration_minutes} minutes

Passenger Information:
- Name: {passenger.full_name}
- Phone: {passenger.phone_number}
- Adults: {booking.transfer_information.adults}
- Children: {booking.transfer_information.children or 0}
- Luggage: {booking.transfer_information.luggage}
{f"- Additional Info: {passenger.additional_information}" if passenger.additional_information else ""}
{vehicle_info}
{"Return Trip Details:" if booking.trip_type == "Return" else ""}
{f"- Return Date: {booking.return_date.strftime('%B %d, %Y')}" if booking.return_date else ""}
{f"- Return Time: {booking.return_time.strftime('%I:%M %p')}" if booking.return_time else ""}

Please log in to your dashboard to view all your bookings:
{dashboard_url}

Please ensure you arrive at the pickup location on time.

Best regards,
First Class Transfer Team
    """.strip()

    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [driver.email],
            fail_silently=False,
        )
        return True

    return False


def send_vehicle_assigned_to_passenger(booking):
    """
    Send email to passenger notifying them that a vehicle has been assigned to their booking.
    """
    passenger = booking.passenger_information
    vehicle = booking.vehicle
    route = booking.route

    if not passenger or not passenger.email_address or not vehicle:
        return False

    subject = f"Vehicle Assigned to Your Booking #{booking.booking_id}"

    message = f"""
Dear {passenger.full_name},

A vehicle has been assigned to your booking.

Booking Details:
- Booking ID: {booking.booking_id}
- Route: {route.from_location} → {route.to_location}
- Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
- Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}

Vehicle Information:
- Type: {vehicle.type}
- Make/Model: {vehicle.make} {vehicle.model}
- Max Passengers: {vehicle.max_passengers}

If you have any questions, please don't hesitate to contact us.

Best regards,
First Class Transfer Team
    """.strip()

    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [passenger.email_address],
            fail_silently=False,
        )
        return True

    return False


def send_booking_updated_to_passenger(booking, changes=None):
    """
    Send email to passenger notifying them that their booking has been updated.
    """
    passenger = booking.passenger_information
    route = booking.route
    driver = booking.driver
    vehicle = booking.vehicle

    if not passenger or not passenger.email_address:
        return False

    subject = f"Booking Updated - #{booking.booking_id}"

    changes_text = ""
    if changes:
        changes_text = "Changes made:\n" + "\n".join([f"- {change}" for change in changes]) + "\n"

    driver_info = ""
    if driver:
        driver_info = f"""
Driver Information:
- Name: {driver.full_name}
- Phone: {driver.phone_number or 'Will be provided'}
"""

    vehicle_info = ""
    if vehicle:
        vehicle_info = f"""
Vehicle Information:
- Type: {vehicle.type}
- Make/Model: {vehicle.make} {vehicle.model}
"""

    message = f"""
Dear {passenger.full_name},

Your booking has been updated. Please review the new details below.

{changes_text}
Updated Booking Details:
- Booking ID: {booking.booking_id}
- Route: {route.from_location} → {route.to_location}
- Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
- Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
- Status: {booking.status}
{driver_info}{vehicle_info}
{"Return Trip Details:" if booking.trip_type == "Return" and booking.return_date else ""}
{f"- Return Date: {booking.return_date.strftime('%B %d, %Y')}" if booking.return_date else ""}
{f"- Return Time: {booking.return_time.strftime('%I:%M %p')}" if booking.return_time else ""}

If you have any questions about these changes, please don't hesitate to contact us.

Best regards,
First Class Transfer Team
    """.strip()

    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [passenger.email_address],
            fail_silently=False,
        )
        return True

    return False


def send_booking_updated_to_driver(booking, changes=None):
    """
    Send email to driver notifying them that a booking they are assigned to has been updated.
    """
    driver = booking.driver
    passenger = booking.passenger_information
    route = booking.route
    vehicle = booking.vehicle

    if not driver or not driver.email:
        return False

    subject = f"Booking Updated - #{booking.booking_id}"

    dashboard_url = f"{settings.FRONTEND_URL}/driver/bookings"

    changes_text = ""
    if changes:
        changes_text = "Changes made:\n" + "\n".join([f"- {change}" for change in changes]) + "\n"

    vehicle_info = ""
    if vehicle:
        vehicle_info = f"""
Vehicle Assigned:
- {vehicle.make} {vehicle.model}
- License Plate: {vehicle.license_plate}
- Type: {vehicle.type}
"""

    message = f"""
Dear {driver.full_name},

A booking you are assigned to has been updated. Please review the new details below.

{changes_text}
Updated Booking Details:
- Booking ID: {booking.booking_id}
- Route: {route.from_location} → {route.to_location}
- Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
- Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
- Estimated Duration: {route.duration_minutes} minutes
- Status: {booking.status}

Passenger Information:
- Name: {passenger.full_name}
- Phone: {passenger.phone_number}
- Adults: {booking.transfer_information.adults}
- Children: {booking.transfer_information.children or 0}
- Luggage: {booking.transfer_information.luggage}
{f"- Additional Info: {passenger.additional_information}" if passenger.additional_information else ""}
{vehicle_info}
{"Return Trip Details:" if booking.trip_type == "Return" and booking.return_date else ""}
{f"- Return Date: {booking.return_date.strftime('%B %d, %Y')}" if booking.return_date else ""}
{f"- Return Time: {booking.return_time.strftime('%I:%M %p')}" if booking.return_time else ""}

Please log in to your dashboard to view all your bookings:
{dashboard_url}

Best regards,
First Class Transfer Team
    """.strip()

    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [driver.email],
            fail_silently=False,
        )
        return True

    return False
