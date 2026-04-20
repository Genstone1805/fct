from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from contextlib import suppress


def _send_html_email(subject, greeting, message, detail, recipient_email):
    """
    Render email.html and send as HTML email.
    """
    context = {
        'title': subject,
        'greeting': greeting,
        'message': mark_safe(message),
        'detail': mark_safe(detail),
    }
    html_message = render_to_string('email.html', context)

    send_mail(
        subject,
        '',
        settings.EMAIL_FROM,
        [recipient_email],
        html_message=html_message,
        fail_silently=False,
    )


def _booking_detail_lines(booking, route, extra_lines=None):
    """Build common booking detail HTML lines."""
    lines = [
        f"<strong>Booking ID:</strong> {booking.booking_id}",
        f"<strong>Route:</strong> {route.from_location} → {route.to_location}",
        f"<strong>Pickup Date:</strong> {booking.pickup_date.strftime('%B %d, %Y')}",
        f"<strong>Pickup Time:</strong> {booking.pickup_time.strftime('%I:%M %p')}",
        f"<strong>Trip Type:</strong> {booking.trip_type}",
    ]
    if extra_lines:
        lines.extend(extra_lines)
    if booking.trip_type == "Return" and booking.return_date:
        lines.append(f"<strong>Return Date:</strong> {booking.return_date.strftime('%B %d, %Y')}")
        lines.append(f"<strong>Return Time:</strong> {booking.return_time.strftime('%I:%M %p') if booking.return_time else 'TBC'}")
    return "<br>".join(lines)


def send_reservation_to_passenger(booking):
    """Send email to passenger confirming their booking has been received."""
    passenger = booking.passenger_information
    route = booking.route

    if not passenger or not passenger.email_address:
        return False

    subject = "New Booking Reservation (Pending Order)"
    greeting = f"Hello {passenger.full_name}"
    message = (
        f"Thank you for your booking. We have received your reservation "
        f"for {booking.pickup_date.strftime('%B %d, %Y')} at "
        f"{booking.pickup_time.strftime('%I:%M %p')} from {route.from_location} "
        f"to {route.to_location}."
        f"<br><br>Our team is now reviewing the details of your reservation."
        f"<br><br>We will confirm your booking shortly and assign your driver "
        f"as soon as everything is finalized."
    )
    detail = _booking_detail_lines(booking, route)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, passenger.email_address)
        return True

    return False


def send_booking_confirmation_to_passenger(booking):
    """Send email to passenger confirming their booking has been received."""
    passenger = booking.passenger_information
    route = booking.route

    if not passenger or not passenger.email_address:
        return False

    subject = f"Booking Received - #{booking.booking_id}"
    greeting = f"Hello {passenger.full_name}"
    message = (
        "Thank you for booking with First Class Transfers! We have received your "
        "booking and it is currently being processed."
        "<br><br><strong>What happens next?</strong><br>"
        "We will assign a driver and a vehicle to your booking shortly and will "
        "keep you updated every step of the way."
        "<br><br><strong>Need to make changes?</strong><br>"
        "If your plans change and you need to reschedule or make any adjustments "
        "to your booking, please don't hesitate to reach out to us."
    )
    detail = _booking_detail_lines(booking, route)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, passenger.email_address)
        return True

    return False


def send_driver_assigned_to_passenger(booking):
    """Send email to passenger notifying them that a driver has been assigned."""
    passenger = booking.passenger_information
    driver = booking.driver
    route = booking.route

    if not passenger or not passenger.email_address or not driver:
        return False

    subject = f"Driver Assigned to Your Booking #{booking.booking_id}"
    greeting = f"Hello {passenger.full_name}"
    message = (
        "Great news! A driver has been assigned to your booking."
        "<br><br>Your driver will be at the pickup location on time. "
        "Please ensure you are ready at the scheduled time."
    )
    extra = [
        f"<br><strong>Driver Name:</strong> {driver.full_name}",
        f"<strong>Driver Phone:</strong> {driver.phone_number or 'Will be provided'}",
    ]
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, passenger.email_address)
        return True

    return False


def send_booking_assigned_to_driver(booking):
    """Send email to driver notifying them that they have been assigned to a booking."""
    driver = booking.driver
    passenger = booking.passenger_information
    route = booking.route
    vehicle = booking.vehicle

    if not driver or not driver.email:
        return False

    subject = f"New Booking Assignment - #{booking.booking_id}"
    dashboard_url = f"{settings.FRONTEND_URL}/driver/bookings"
    greeting = f"Hello {driver.full_name}"
    message = (
        "You have been assigned to a new booking."
        "<br><br>Please ensure you arrive at the pickup location on time."
        f"<br><br>View your dashboard: <a href='{dashboard_url}'>{dashboard_url}</a>"
    )
    extra = [
        f"<strong>Estimated Duration:</strong> {route.duration_minutes} minutes",
        f"<br><strong>Passenger:</strong> {passenger.full_name}",
        f"<strong>Phone:</strong> {passenger.phone_number}",
        f"<strong>Adults:</strong> {booking.transfer_information.adults}",
        f"<strong>Children:</strong> {booking.transfer_information.children or 0}",
        f"<strong>Luggage:</strong> {booking.transfer_information.luggage}",
    ]
    if passenger.additional_information:
        extra.append(f"<strong>Additional Info:</strong> {passenger.additional_information}")
    if vehicle:
        extra.append(f"<br><strong>Vehicle:</strong> {vehicle.make} {vehicle.model}")
        extra.append(f"<strong>License Plate:</strong> {vehicle.license_plate}")
        extra.append(f"<strong>Type:</strong> {vehicle.type}")
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, driver.email)
        return True

    return False


def send_vehicle_assigned_to_passenger(booking):
    """Send email to passenger notifying them that a vehicle has been assigned."""
    passenger = booking.passenger_information
    vehicle = booking.vehicle
    route = booking.route

    if not passenger or not passenger.email_address or not vehicle:
        return False

    subject = f"Vehicle Assigned to Your Booking #{booking.booking_id}"
    greeting = f"Hello {passenger.full_name}"
    message = "A vehicle has been assigned to your booking."
    extra = [
        f"<br><strong>Vehicle Type:</strong> {vehicle.type}",
        f"<strong>Make/Model:</strong> {vehicle.make} {vehicle.model}",
        f"<strong>Max Passengers:</strong> {vehicle.max_passengers}",
    ]
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, passenger.email_address)
        return True

    return False


def send_assignment_to_passenger(booking):
    """Send email to passenger notifying them that both driver and vehicle have been assigned."""
    passenger = booking.passenger_information
    driver = booking.driver
    vehicle = booking.vehicle
    route = booking.route

    if not passenger or not passenger.email_address or not driver or not vehicle:
        return False

    subject = f"Your Booking #{booking.booking_id} is Confirmed - Driver & Vehicle Assigned"
    greeting = f"Hello {passenger.full_name}"
    message = (
        "Great news! Your booking has been confirmed. A driver and vehicle have been assigned."
        "<br><br>Your driver will arrive at the pickup location on time. "
        "Please ensure you are ready at the scheduled time."
    )
    extra = [
        f"<br><strong>Driver:</strong> {driver.full_name}",
        f"<strong>Driver Phone:</strong> {driver.phone_number or 'Will be provided'}",
        f"<br><strong>Vehicle Type:</strong> {vehicle.type}",
        f"<strong>Make/Model:</strong> {vehicle.make} {vehicle.model}",
        f"<strong>License Plate:</strong> {vehicle.license_plate}",
        f"<strong>Max Passengers:</strong> {vehicle.max_passengers}",
        f"<br><strong>Payment Method:</strong> {booking.payment_type}",
        f"<strong>Payment Status:</strong> {booking.payment_status}",
    ]
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, passenger.email_address)
        return True

    return False


def send_assignment_to_driver(booking):
    """Send email to driver notifying them about the booking assignment with vehicle info."""
    driver = booking.driver
    passenger = booking.passenger_information
    route = booking.route
    vehicle = booking.vehicle

    if not driver or not driver.email or not vehicle:
        return False

    subject = f"New Booking Assignment - #{booking.booking_id}"
    dashboard_url = f"{settings.FRONTEND_URL}/driver/bookings"
    greeting = f"Hello {driver.full_name}"
    message = (
        "You have been assigned to a new booking."
        "<br><br>Please ensure you arrive at the pickup location on time with the assigned vehicle."
        f"<br><br>View your dashboard: <a href='{dashboard_url}'>{dashboard_url}</a>"
    )
    extra = [
        f"<strong>Estimated Duration:</strong> {route.duration_minutes} minutes",
        f"<br><strong>Passenger:</strong> {passenger.full_name}",
        f"<strong>Phone:</strong> {passenger.phone_number}",
        f"<strong>Email:</strong> {passenger.email_address}",
        f"<strong>Adults:</strong> {booking.transfer_information.adults}",
        f"<strong>Children:</strong> {booking.transfer_information.children or 0}",
        f"<strong>Luggage:</strong> {booking.transfer_information.luggage}",
    ]
    if passenger.additional_information:
        extra.append(f"<strong>Additional Info:</strong> {passenger.additional_information}")
    extra.extend([
        f"<br><strong>Vehicle Type:</strong> {vehicle.type}",
        f"<strong>Make/Model:</strong> {vehicle.make} {vehicle.model}",
        f"<strong>License Plate:</strong> {vehicle.license_plate}",
    ])
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, driver.email)
        return True

    return False


def send_booking_updated_to_passenger(booking, changes=None):
    """Send email to passenger notifying them that their booking has been updated."""
    passenger = booking.passenger_information
    route = booking.route
    driver = booking.driver
    vehicle = booking.vehicle

    if not passenger or not passenger.email_address:
        return False

    subject = f"Booking Updated - #{booking.booking_id}"
    greeting = f"Hello {passenger.full_name}"

    changes_html = ""
    if changes:
        changes_html = "<br><br><strong>Changes made:</strong><br>" + "<br>".join(f"• {c}" for c in changes)

    message = f"Your booking has been updated. Please review the new details below.{changes_html}"

    extra = [f"<strong>Status:</strong> {booking.booking_status}"]
    if driver:
        extra.append(f"<br><strong>Driver:</strong> {driver.full_name}")
        extra.append(f"<strong>Driver Phone:</strong> {driver.phone_number or 'Will be provided'}")
    if vehicle:
        extra.append(f"<br><strong>Vehicle Type:</strong> {vehicle.type}")
        extra.append(f"<strong>Make/Model:</strong> {vehicle.make} {vehicle.model}")
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, passenger.email_address)
        return True

    return False


def send_booking_updated_to_driver(booking, changes=None):
    """Send email to driver notifying them that a booking they are assigned to has been updated."""
    driver = booking.driver
    passenger = booking.passenger_information
    route = booking.route
    vehicle = booking.vehicle

    if not driver or not driver.email:
        return False

    subject = f"Booking Updated - #{booking.booking_id}"
    dashboard_url = f"{settings.FRONTEND_URL}/driver/bookings"
    greeting = f"Hello {driver.full_name}"

    changes_html = ""
    if changes:
        changes_html = "<br><br><strong>Changes made:</strong><br>" + "<br>".join(f"• {c}" for c in changes)

    message = (
        f"A booking you are assigned to has been updated. Please review the new details below.{changes_html}"
        f"<br><br>View your dashboard: <a href='{dashboard_url}'>{dashboard_url}</a>"
    )

    extra = [
        f"<strong>Estimated Duration:</strong> {route.duration_minutes} minutes",
        f"<strong>Status:</strong> {booking.booking_status}",
        f"<br><strong>Passenger:</strong> {passenger.full_name}",
        f"<strong>Phone:</strong> {passenger.phone_number}",
        f"<strong>Adults:</strong> {booking.transfer_information.adults}",
        f"<strong>Children:</strong> {booking.transfer_information.children or 0}",
        f"<strong>Luggage:</strong> {booking.transfer_information.luggage}",
    ]
    if passenger.additional_information:
        extra.append(f"<strong>Additional Info:</strong> {passenger.additional_information}")
    if vehicle:
        extra.append(f"<br><strong>Vehicle:</strong> {vehicle.make} {vehicle.model}")
        extra.append(f"<strong>License Plate:</strong> {vehicle.license_plate}")
        extra.append(f"<strong>Type:</strong> {vehicle.type}")
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, driver.email)
        return True

    return False


def send_status_change_to_passenger(booking, old_status, new_status):
    """Send email to passenger notifying them that their booking status has changed."""
    passenger = booking.passenger_information
    route = booking.route

    if not passenger or not passenger.email_address:
        return False

    status_messages = {
        'Completed': 'Your trip has been completed. Thank you for choosing First Class Transfers!',
        'Cancelled': 'Your booking has been cancelled. If you did not request this cancellation, please contact us immediately.',
    }

    subject = f"Booking {new_status} - #{booking.booking_id}"
    greeting = f"Hello {passenger.full_name}"
    message = status_messages.get(new_status, f'Your booking status has been updated to {new_status}.')
    extra = [
        f"<strong>Previous Status:</strong> {old_status}",
        f"<strong>New Status:</strong> {new_status}",
    ]
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, passenger.email_address)
        return True

    return False


def send_status_change_to_driver(booking, old_status, new_status):
    """Send email to driver notifying them that a booking status has changed."""
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
    greeting = f"Hello {driver.full_name}"
    message = (
        f"{status_messages.get(new_status, f'A booking you were assigned to has been updated to {new_status}.')}"
        f"<br><br>View your dashboard: <a href='{dashboard_url}'>{dashboard_url}</a>"
    )
    extra = [
        f"<strong>Passenger:</strong> {passenger.full_name}",
        f"<strong>Previous Status:</strong> {old_status}",
        f"<strong>New Status:</strong> {new_status}",
    ]
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, driver.email)
        return True

    return False


def send_payment_status_update_to_passenger(booking, old_status, new_status):
    """Send email to passenger notifying them that their payment status has changed."""
    passenger = booking.passenger_information
    route = booking.route

    if not passenger or not passenger.email_address:
        return False

    status_messages = {
        'paid': 'Your payment has been confirmed. Thank you!',
        'paid 20%': 'We have received your 20% deposit. The remaining balance is due on the day of your trip.',
        'failed': 'Unfortunately, your payment has failed. Please contact us to resolve this.',
        'cancelled': 'Your payment has been cancelled.',
        'expired': 'Your payment has expired. Please contact us to make a new payment.',
        'pending': 'Your payment is pending. We will notify you once it has been processed.',
    }

    subject = f"Payment Update - Booking #{booking.booking_id}"
    greeting = f"Hello {passenger.full_name}"
    message = status_messages.get(new_status, f'Your payment status has been updated to {new_status}.')
    extra = [
        f"<br><strong>Payment Method:</strong> {booking.payment_type}",
        f"<strong>Previous Status:</strong> {old_status}",
        f"<strong>New Status:</strong> {new_status}",
    ]
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, passenger.email_address)
        return True

    return False
