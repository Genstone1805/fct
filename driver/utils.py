import os
from django.conf import settings
from django.utils import timezone
from contextlib import suppress
from django.core.mail import send_mail

def signup_email_to_driver(user, generated_password):
    # Send email with credentials
    subject = "Welcome to First Class Transfer - Your Login Credentials"  

    message = f"""
        Hello {user.full_name or 'there'},

        Welcome to First Class Transfer!  
        You’ve been successfully onboarded as a **Driver** on our platform.

        Below are your login details:

        Email: {user.email}  
        Temporary Password: {generated_password}

        Role: Driver  

        Next steps:
        - visit https://firstclasstransfers.eu/drivers/login to login into our site

        You’re now part of our trusted driver network, and we’re excited to have you on board. If you need support, our team is ready to assist.

        Drive safe and deliver excellence.

        Best regards,  
        First Class Transfer Team
    """
    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [user.email],
            fail_silently=False,
        )

def update_driver_info_email_to_admin(driver, user):
    # Send email with credentials
    subject = f"{driver.full_name} Information Updated"  

    message = f"""
        Hello,

        This is to notify you that the profile information of a driver on the First Class Transfer platform has been updated.

        Driver Details

        Name: {driver.full_name}

        Email: {driver.email}
        
        Updated By: {user.full_name}

        The updated details are now live in the system.

        Next Steps
        If verification, approval, or further adjustments are required, please log in to the admin dashboard using the link below:

        👉 https://firstclasstransfers.eu/admin/login

        All driver profile management actions can be handled directly from the dashboard.

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

def signup_email_to_admin(user, admin):
    # Send email with credentials
    subject = "New Driver Account Added"  

    message = f"""
        Hello,

        This is to inform you that a new driver account has been successfully created on the First Class Transfer platform.

        Driver Details

        Name: {user.full_name}

        Email: {user.email}
        Created By: {admin.email}

        The driver has been onboarded and provided with initial login credentials. They have been instructed to update their password upon first login in line with security best practices.

        Next Steps
        If any verification, profile updates, or role adjustments are required, please log in to the admin dashboard using the link below:

        👉 https://firstclasstransfers.eu/admin/login

        All driver management and verification actions can be completed directly from the dashboard.

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

def delete_driver_info_email_to_admin(driver, user):
    # Send email with credentials
    subject = f"{user.full_name} Account Deleted"  

    message = f"""
        Hello,

        This is to notify you that a driver account has been deleted from the First Class Transfer platform.

        Driver Details

        Name: {driver.full_name}

        Email: {driver.email}
        
        Deleted By: {user.full_name}

        The driver has been onboarded and provided with initial login credentials. They have been instructed to update their password upon first login in line with security best practices.

        Next Steps
        If any verification, profile updates, or role adjustments are required, please log in to the admin dashboard using the link below:

        👉 https://firstclasstransfers.eu/admin/login

        All driver management and verification actions can be completed directly from the dashboard.

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