from django.conf import settings
from contextlib import suppress
from django.core.mail import send_mail



def route_created_email_to_admin(user, route):
    # Send email with credentials
    subject = "{route.from_location} to {route.to_location} Created on the Platform" 

    message = f"""
        Hello,

        This is to inform you that a new route has been successfully created on the First Class Transfer platform.

        Route Details

        Route from: {route.from_location}
        Route to: {route.to_location}

        Created By: {user.full_name}


        The route is now live in the system. If any adjustments, validations, or approvals are required, please log in to the admin dashboard using the link below:

        👉 https://firstclasstransfers.eu/admin/login

        All route configurations and permissions can be managed directly from the dashboard.

        Best regards,
        First Class Transfer Team
    """
    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [settings.EMAIL_FROM],
            fail_silently=False,
        )

def update_created_email_to_admin(user, route):
    # Send email with credentials
    subject = "{route.from_location} to {route.to_location} Updated" 

    message = f"""
        Hello,

        This is to inform you that a new route has been successfully created on the First Class Transfer platform.

        Route Details

        Route from: {route.from_location}
        Route to: {route.to_location}

        Updated By: {user.full_name}


        The route is now live in the system. If any adjustments, validations, or approvals are required, please log in to the admin dashboard using the link below:

        👉 https://firstclasstransfers.eu/admin/login

        All route configurations and permissions can be managed directly from the dashboard.

        Best regards,
        First Class Transfer Team
    """
    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [settings.EMAIL_FROM],
            fail_silently=False,
        )