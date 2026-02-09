import os
from django.conf import settings
from django.utils import timezone
from contextlib import suppress
from django.core.mail import send_mail

def vehicle_create_email_to_admin(vehicle, user):
    # Send email with credentials
    subject = "New Vehicle Added to the Platform"  

    message = f"""
        Hello,

        This is to inform you that a new vehicle has been successfully added to the First Class Transfer platform.

        Vehicle Details:

        Added By: {user.full_name} ({user.email})

        License Plate: {vehicle.license_plate}

        Make: {vehicle.make}

        Model: {vehicle.model}

        Year: {vehicle. year}

        Color: {vehicle.color}

        Type: {vehicle.type}

        Max Passengers: {vehicle.max_passengers}


        If verification, assignment to bookings, or updates are required, please log in to the admin dashboard:

        👉 https://firstclasstransfers.eu/admin/login

        All vehicle management, assignment, and verification actions can be handled directly from the dashboard.

        Best regards,
        First Class Transfer Team
    """
    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [user.EMAIL_FROM],
            fail_silently=False,
        )
def vehicle_update_email_to_admin(vehicle, user):
    # Send email with credentials
    subject = "Vehicle Information Updated"  

    message = f"""
        Hello,

        This is to notify you that a vehicle's information has been updated on the First Class Transfer platform.

        Deleted Vehicle Details:

        Deleted By: {user.full_name} ({user.email})

        License Plate: {vehicle.license_plate}

        Make: {vehicle.make}

        Model: {vehicle.model}

        Year: {vehicle. year}

        Color: {vehicle.color}

        Type: {vehicle.type}

        Max Passengers: {vehicle.max_passengers}


        If verification, assignment to bookings, or updates are required, please log in to the admin dashboard:

        👉 https://firstclasstransfers.eu/admin/login

        All vehicle management, assignment, and verification actions can be handled directly from the dashboard.

        Best regards,
        First Class Transfer Team
    """
    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [user.EMAIL_FROM],
            fail_silently=False,
        )
def vehicle_delete_email_to_admin(vehicle, user):
    # Send email with credentials
    subject = "Vehicle Deleted from the Platform"  

    message = f"""
        Hello,

        This is to notify you that a vehicle has been deleted from the First Class Transfer platform.

        Deleted Vehicle Details:

        Deleted By: {user.full_name} ({user.email})

        License Plate: {vehicle.license_plate}

        Make: {vehicle.make}

        Model: {vehicle.model}

        Year: {vehicle. year}

        Color: {vehicle.color}

        Type: {vehicle.type}

        Max Passengers: {vehicle.max_passengers}


        If verification, assignment to bookings, or updates are required, please log in to the admin dashboard:

        👉 https://firstclasstransfers.eu/admin/login

        All vehicle management, assignment, and verification actions can be handled directly from the dashboard.

        Best regards,
        First Class Transfer Team
    """
    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [user.EMAIL_FROM],
            fail_silently=False,
        )
