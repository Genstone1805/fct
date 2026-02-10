from django.conf import settings
from contextlib import suppress

from booking.emails import _send_html_email


ADMIN_DASHBOARD_URL = "https://firstclasstransfers.eu/admin/login"


def route_created_email_to_admin(user, route):
    subject = f"{route.from_location} to {route.to_location} Created on the Platform"
    greeting = "Hello Admin"
    message = (
        "A new route has been successfully created on the First Class Transfers platform."
        "<br><br>The route is now live in the system."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    detail = (
        f"<strong>From:</strong> {route.from_location}<br>"
        f"<strong>To:</strong> {route.to_location}<br>"
        f"<strong>Created By:</strong> {user.full_name}"
    )

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)


def update_created_email_to_admin(user, route):
    subject = f"{route.from_location} to {route.to_location} Updated"
    greeting = "Hello Admin"
    message = (
        "A route has been updated on the First Class Transfers platform."
        "<br><br>The updated route is now live in the system."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    detail = (
        f"<strong>From:</strong> {route.from_location}<br>"
        f"<strong>To:</strong> {route.to_location}<br>"
        f"<strong>Updated By:</strong> {user.full_name}"
    )

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)
