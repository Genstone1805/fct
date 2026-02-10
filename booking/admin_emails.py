from django.conf import settings
from contextlib import suppress

from .emails import _send_html_email, _booking_detail_lines


ADMIN_DASHBOARD_URL = "https://firstclasstransfers.eu/admin/login"


def send_reservation_to_admin():
    subject = "New Reservation Submitted – Action Required"
    greeting = "Hello Admin"
    message = (
        "A new reservation has just been created in the system and is currently pending confirmation."
        "<br><br>Please log in to the admin dashboard to review the booking details, "
        "confirm payment status, and proceed with driver assignment."
        "<br><br>Before proceeding with driver assignment, please carefully verify and confirm "
        "the payment in the Revolut dashboard to ensure the transaction has been successfully "
        "completed and cleared."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    detail = "A new reservation is awaiting review and driver assignment."

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)
        return True

    return False


def send_booking_confirmation_to_admin(booking):
    passenger = booking.passenger_information
    route = booking.route

    if not passenger or not passenger.email_address:
        return False

    subject = "New Booking Received – Action Required"
    greeting = "Hello Admin"
    message = (
        "A new booking has been successfully received on the First Class Transfers platform "
        "and is ready for review."
        "<br><br><strong>Next Steps</strong><br>"
        "Please assign a driver and vehicle to this booking and review any special requirements "
        "to ensure timely fulfillment."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    extra = [
        f"<strong>Passenger:</strong> {passenger.full_name}",
        f"<strong>Email:</strong> {passenger.email_address}",
    ]
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)
        return True

    return False


def send_booking_updated_to_admin(booking, user, changes=None):
    passenger = booking.passenger_information
    route = booking.route
    driver = booking.driver
    vehicle = booking.vehicle

    if not passenger or not passenger.email_address:
        return False

    subject = "Booking Updated – Review Required"
    greeting = "Hello Admin"

    changes_html = ""
    if changes:
        changes_html = "<br><br><strong>Changes made:</strong><br>" + "<br>".join(f"• {c}" for c in changes)

    message = (
        f"An existing booking on the First Class Transfers platform has been updated.{changes_html}"
        "<br><br>Please review the updated booking to ensure all changes align with operational requirements."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )

    extra = [
        f"<strong>Status:</strong> {booking.booking_status}",
        f"<strong>Updated By:</strong> {user.full_name}",
        f"<br><strong>Passenger:</strong> {passenger.full_name}",
        f"<strong>Email:</strong> {passenger.email_address}",
    ]
    if driver:
        extra.append(f"<br><strong>Driver:</strong> {driver.full_name}")
        extra.append(f"<strong>Driver Phone:</strong> {driver.phone_number or 'Will be provided'}")
    if vehicle:
        extra.append(f"<br><strong>Vehicle Type:</strong> {vehicle.type}")
        extra.append(f"<strong>Make/Model:</strong> {vehicle.make} {vehicle.model}")
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)
        return True

    return False


def send_assignment_to_admin(booking, user):
    passenger = booking.passenger_information
    driver = booking.driver
    vehicle = booking.vehicle
    route = booking.route

    if not passenger or not passenger.email_address or not driver or not vehicle:
        return False

    subject = f"Driver & Vehicle Assigned to Booking #{booking.booking_id}"
    greeting = "Hello Admin"
    message = (
        "A driver and vehicle have been successfully assigned to a booking."
        "<br><br>The booking is now fully confirmed and operationally ready."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    extra = [
        f"<strong>Assigned By:</strong> {user.full_name}",
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
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)
        return True

    return False


def send_status_change_to_admin(user, booking, old_status, new_status):
    passenger = booking.passenger_information
    route = booking.route

    if not passenger or not passenger.email_address:
        return False

    subject = f"Booking {new_status} - #{booking.booking_id}"
    greeting = "Hello Admin"
    message = (
        "The status of a booking has been updated. The passenger has been notified of this change."
        "<br><br>Please review the booking to confirm that the updated status aligns with "
        "operational and business requirements."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    extra = [
        f"<strong>Previous Status:</strong> {old_status}",
        f"<strong>New Status:</strong> {new_status}",
        f"<strong>Changed By:</strong> {user.full_name}",
        f"<br><strong>Passenger:</strong> {passenger.full_name}",
        f"<strong>Email:</strong> {passenger.email_address}",
    ]
    detail = _booking_detail_lines(booking, route, extra_lines=extra)

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)
        return True

    return False
