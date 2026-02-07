from django.core.mail import send_mail
from django.conf import settings
from contextlib import suppress


def send_booking_confirmation_to_passenger(booking):
    """
    Send email to passenger confirming their booking has been received.
    """
    passenger = booking.passenger_information
    route = booking.route

    if not passenger or not passenger.email_address:
        return False

    subject = f"Booking Received - #{booking.booking_id}"

    return_info = ""
    if booking.trip_type == "Return" and booking.return_date:
        return_info = f"""
        Return Trip Details:
        - Return Date: {booking.return_date.strftime('%B %d, %Y')}
        - Return Time: {booking.return_time.strftime('%I:%M %p') if booking.return_time else 'TBC'}
        """

    message = f"""
        Dear {passenger.full_name},

        Thank you for booking with First Class Transfer! We have received your booking and it is currently being processed.

        Booking Details:
        - Booking ID: {booking.booking_id}
        - Route: {route.from_location} → {route.to_location}
        - Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
        - Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
        - Trip Type: {booking.trip_type}
        {return_info}
        What happens next?
        We will assign a driver and a vehicle to your booking shortly and will keep you updated every step of the way.

        Need to make changes?
        If your plans change and you need to reschedule or make any adjustments to your booking, please don't hesitate to reach out to us. We're happy to help accommodate any changes.

        If you have any questions, feel free to contact us at any time.

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


def send_assignment_to_passenger(booking):
    """
    Send email to passenger notifying them that both driver and vehicle have been assigned.
    Includes complete driver and vehicle information.
    """
    passenger = booking.passenger_information
    driver = booking.driver
    vehicle = booking.vehicle
    route = booking.route

    if not passenger or not passenger.email_address or not driver or not vehicle:
        return False

    subject = f"Your Booking #{booking.booking_id} is Confirmed - Driver & Vehicle Assigned"

    message = f"""
        Dear {passenger.full_name},

        Great news! Your booking has been confirmed. A driver and vehicle have been assigned.

        Booking Details:
        - Booking ID: {booking.booking_id}
        - Route: {route.from_location} → {route.to_location}
        - Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
        - Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
        - Trip Type: {booking.trip_type}

        Driver Information:
        - Name: {driver.full_name}
        - Phone: {driver.phone_number or 'Will be provided'}

        Vehicle Information:
        - Type: {vehicle.type}
        - Make/Model: {vehicle.make} {vehicle.model}
        - License Plate: {vehicle.license_plate}
        - Max Passengers: {vehicle.max_passengers}

        {"Return Trip Details:" if booking.trip_type == "Return" and booking.return_date else ""}
        {f"- Return Date: {booking.return_date.strftime('%B %d, %Y')}" if booking.return_date else ""}
        {f"- Return Time: {booking.return_time.strftime('%I:%M %p')}" if booking.return_time else ""}

        Your driver will arrive at the pickup location on time. Please ensure you are ready at the scheduled time.

        Payment Information:
        - Payment Method: {booking.payment_type}
        - Payment Status: {booking.payment_status}

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


def send_assignment_to_driver(booking):
    """
    Send email to driver notifying them about the booking assignment with vehicle info.
    """
    driver = booking.driver
    passenger = booking.passenger_information
    route = booking.route
    vehicle = booking.vehicle

    if not driver or not driver.email or not vehicle:
        return False

    subject = f"New Booking Assignment - #{booking.booking_id}"

    dashboard_url = f"{settings.FRONTEND_URL}/driver/bookings"

    message = f"""
        Dear {driver.full_name},

        You have been assigned to a new booking.

        Booking Details:
        - Booking ID: {booking.booking_id}
        - Route: {route.from_location} → {route.to_location}
        - Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
        - Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
        - Estimated Duration: {route.duration_minutes} minutes
        - Trip Type: {booking.trip_type}

        Passenger Information:
        - Name: {passenger.full_name}
        - Phone: {passenger.phone_number}
        - Email: {passenger.email_address}
        - Adults: {booking.transfer_information.adults}
        - Children: {booking.transfer_information.children or 0}
        - Luggage: {booking.transfer_information.luggage}
        {f"- Additional Info: {passenger.additional_information}" if passenger.additional_information else ""}

        Vehicle Assigned to You:
        - Type: {vehicle.type}
        - Make/Model: {vehicle.make} {vehicle.model}
        - License Plate: {vehicle.license_plate}

        {"Return Trip Details:" if booking.trip_type == "Return" and booking.return_date else ""}
        {f"- Return Date: {booking.return_date.strftime('%B %d, %Y')}" if booking.return_date else ""}
        {f"- Return Time: {booking.return_time.strftime('%I:%M %p')}" if booking.return_time else ""}

        Please log in to your dashboard to view all your bookings:
        {dashboard_url}

        Please ensure you arrive at the pickup location on time with the assigned vehicle.

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


def send_status_change_to_passenger(booking, old_status, new_status):
    """
    Send email to passenger notifying them that their booking status has changed.
    """
    passenger = booking.passenger_information
    route = booking.route

    if not passenger or not passenger.email_address:
        return False

    status_messages = {
        'Completed': 'Your trip has been completed. Thank you for choosing First Class Transfer!',
        'Cancelled': 'Your booking has been cancelled. If you did not request this cancellation, please contact us immediately.',
    }

    subject = f"Booking {new_status} - #{booking.booking_id}"

    message = f"""
        Dear {passenger.full_name},

        {status_messages.get(new_status, f'Your booking status has been updated to {new_status}.')}

        Booking Details:
        - Booking ID: {booking.booking_id}
        - Route: {route.from_location} → {route.to_location}
        - Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
        - Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
        - Previous Status: {old_status}
        - New Status: {new_status}

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


def send_status_change_to_driver(booking, old_status, new_status):
    """
    Send email to driver notifying them that a booking status has changed.
    """
    driver = booking.driver
    passenger = booking.passenger_information
    route = booking.route

    if not driver or not driver.email:
        return False

    status_messages = {
        'Completed': 'This booking has been marked as completed. Great job!',
        'Cancelled': 'This booking has been cancelled.',
    }

    subject = f"Booking {new_status} - #{booking.booking_id}"

    dashboard_url = f"{settings.FRONTEND_URL}/driver/bookings"

    message = f"""
Dear {driver.full_name},

{status_messages.get(new_status, f'A booking you were assigned to has been updated to {new_status}.')}

Booking Details:
- Booking ID: {booking.booking_id}
- Route: {route.from_location} → {route.to_location}
- Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
- Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
- Passenger: {passenger.full_name}
- Previous Status: {old_status}
- New Status: {new_status}

Please log in to your dashboard to view your bookings:
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
