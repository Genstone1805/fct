from django.conf import settings
from contextlib import suppress

from booking.emails import _send_html_email


ADMIN_DASHBOARD_URL = "https://firstclasstransfers.eu/admin/login"


def _vehicle_detail(vehicle, user, action_label):
    """Build common vehicle detail HTML."""
    return (
        f"<strong>{action_label}:</strong> {user.full_name} ({user.email})<br>"
        f"<strong>License Plate:</strong> {vehicle.license_plate}<br>"
        f"<strong>Make:</strong> {vehicle.make}<br>"
        f"<strong>Model:</strong> {vehicle.model}<br>"
        f"<strong>Year:</strong> {vehicle.year}<br>"
        f"<strong>Color:</strong> {vehicle.color}<br>"
        f"<strong>Type:</strong> {vehicle.type}<br>"
        f"<strong>Max Passengers:</strong> {vehicle.max_passengers}"
    )


def vehicle_create_email_to_admin(vehicle, user):
    subject = "New Vehicle Added to the Platform"
    greeting = "Hello Admin"
    message = (
        "A new vehicle has been successfully added to the First Class Transfers platform."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    detail = _vehicle_detail(vehicle, user, "Added By")

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)


def vehicle_update_email_to_admin(vehicle, user):
    subject = "Vehicle Information Updated"
    greeting = "Hello Admin"
    message = (
        "A vehicle's information has been updated on the First Class Transfers platform."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    detail = _vehicle_detail(vehicle, user, "Updated By")

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)


def vehicle_delete_email_to_admin(vehicle, user):
    subject = "Vehicle Deleted from the Platform"
    greeting = "Hello Admin"
    message = (
        "A vehicle has been deleted from the First Class Transfers platform."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    detail = _vehicle_detail(vehicle, user, "Deleted By")

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)
