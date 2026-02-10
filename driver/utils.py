from django.conf import settings
from contextlib import suppress

from booking.emails import _send_html_email


ADMIN_DASHBOARD_URL = "https://firstclasstransfers.eu/admin/login"


def signup_email_to_driver(user, generated_password):
    subject = "Welcome to First Class Transfer - Your Login Credentials"
    greeting = f"Hello {user.full_name or 'there'}"
    message = (
        "Welcome to First Class Transfers! You've been successfully onboarded as a Driver on our platform."
        "<br><br>Please visit the link below to log in:"
        "<br><a href='https://firstclasstransfers.eu/drivers/login'>https://firstclasstransfers.eu/drivers/login</a>"
        "<br><br>You're now part of our trusted driver network. Drive safe and deliver excellence."
    )
    detail = (
        f"<strong>Email:</strong> {user.email}<br>"
        f"<strong>Temporary Password:</strong> {generated_password}<br>"
        f"<strong>Role:</strong> Driver"
    )

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, user.email)


def update_driver_info_email_to_admin(driver, user):
    subject = f"{driver.full_name} Information Updated"
    greeting = "Hello Admin"
    message = (
        "The profile information of a driver on the First Class Transfers platform has been updated."
        "<br><br>The updated details are now live in the system."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    detail = (
        f"<strong>Name:</strong> {driver.full_name}<br>"
        f"<strong>Email:</strong> {driver.email}<br>"
        f"<strong>Updated By:</strong> {user.full_name}"
    )

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)


def signup_email_to_admin(user, admin):
    subject = "New Driver Account Added"
    greeting = "Hello Admin"
    message = (
        "A new driver account has been successfully created on the First Class Transfers platform."
        "<br><br>The driver has been onboarded and provided with initial login credentials."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    detail = (
        f"<strong>Name:</strong> {user.full_name}<br>"
        f"<strong>Email:</strong> {user.email}<br>"
        f"<strong>Created By:</strong> {admin.email}"
    )

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)


def delete_driver_info_email_to_admin(driver, user):
    subject = f"{driver.full_name} Account Deleted"
    greeting = "Hello Admin"
    message = (
        "A driver account has been deleted from the First Class Transfers platform."
        f"<br><br><a href='{ADMIN_DASHBOARD_URL}'>{ADMIN_DASHBOARD_URL}</a>"
    )
    detail = (
        f"<strong>Name:</strong> {driver.full_name}<br>"
        f"<strong>Email:</strong> {driver.email}<br>"
        f"<strong>Deleted By:</strong> {user.full_name}"
    )

    with suppress(Exception):
        _send_html_email(subject, greeting, message, detail, settings.EMAIL_FROM)
