from django.conf import settings
from contextlib import suppress
from django.core.mail import send_mail



def send_reservation_to_admin():

    subject = f"New Reservation Submitted – Action Required"


    message = f"""
        Dear Admin,

        This is to notify you that a new reservation has just been created in the system and is currently pending confirmation.

        Please log in to the admin dashboard to review the booking details, confirm payment status, and proceed with driver assignment.
        
        Before proceeding with driver assignment, please carefully verify and confirm the payment in the Revolut dashboard to ensure the transaction has been successfully completed and cleared.

        Once payment confirmation is validated, kindly proceed to assign a driver via the admin dashboard to maintain service continuity and delivery timelines.

        Thank you for your prompt attention.

        Kind regards,
        First Class Transfers
    """.strip()

    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [settings.EMAIL_FROM],
            fail_silently=False,
        )
        return True

    return False


def send_booking_confirmation_to_admin(booking):
    
    passenger = booking.passenger_information
    route = booking.route
    if not passenger or not passenger.email_address:
        return False
    
    return_info = ""
    if booking.trip_type == "Return" and booking.return_date:
        return_info = f"""
        Return Trip Details:
        - Return Date: {booking.return_date.strftime('%B %d, %Y')}
        - Return Time: {booking.return_time.strftime('%I:%M %p') if booking.return_time else 'TBC'}
        """
        
    # Send email with credentials
    subject = "New Booking Received – Action Required" 

    message = f"""
        Hello,

        A new booking has been successfully received on the First Class Transfer platform and is ready for review.
        
        Booking Summary:
        - Booking ID: {booking.booking_id}
        - Route: {route.from_location} → {route.to_location}
        - Passenger Name: {passenger.full_name}
        - Passenger Email: {passenger.email_address}
        - Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
        - Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
        - Trip Type: {booking.trip_type}
        {return_info}

        Next Steps
        Please assign a driver and vehicle to this booking and review any special requirements to ensure timely fulfillment.

        If any adjustments or updates are required, log in to the admin dashboard using the link below:

        👉 https://firstclasstransfers.eu/admin/login

        All booking management actions can be completed directly from the dashboard.

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

def send_booking_updated_to_admin(booking, user, changes=None,):
    """
    Send email to passenger notifying them that their booking has been updated.
    """
    passenger = booking.passenger_information
    route = booking.route
    driver = booking.driver
    vehicle = booking.vehicle

    if not passenger or not passenger.email_address:
        return False

    subject = "Booking Updated – Review Required"

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
        Hello,

        This is to notify you that an existing booking on the First Class Transfer platform has been updated.

        {changes_text}
        Updated Booking Overview:
        - Booking ID: {booking.booking_id}
        - Route: {route.from_location} → {route.to_location}
        - passenger Name: {passenger.full_name}
        - passenger Email: {passenger.email_address}
        - Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
        - Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
        - Status: {booking.booking_status}
        - Updated By {user.full_name}
        {driver_info}{vehicle_info}
        {"Return Trip Details:" if booking.trip_type == "Return" and booking.return_date else ""}
        {f"- Return Date: {booking.return_date.strftime('%B %d, %Y')}" if booking.return_date else ""}
        {f"- Return Time: {booking.return_time.strftime('%I:%M %p')}" if booking.return_time else ""}

        Please review the updated booking to ensure all changes align with operational requirements.
        If further adjustments, reassignment, or validation are needed, log in to the admin dashboard using the link below:

        👉 https://firstclasstransfers.eu/admin/login

        All booking modifications and assignments can be managed directly from the dashboard.
            """.strip()

    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [settings.EMAIL_FROM],
            fail_silently=False,
        )
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

    message = f"""
        Hello,

        This is to inform you that a driver and vehicle have been successfully assigned to a booking on the First Class Transfer platform.

        Booking Details:
        - Booking ID: {booking.booking_id}
        - Route: {route.from_location} → {route.to_location}
        - Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
        - Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
        - Trip Type: {booking.trip_type}

        Driver Information:
        - Name: {driver.full_name}
        - Phone: {driver.phone_number or 'Will be provided'}
        - Assigned By {user.full_name}

        Vehicle Information:
        - Type: {vehicle.type}
        - Make/Model: {vehicle.make} {vehicle.model}
        - License Plate: {vehicle.license_plate}
        - Max Passengers: {vehicle.max_passengers}
        - Assigned By {user.full_name}

        {"Return Trip Details:" if booking.trip_type == "Return" and booking.return_date else ""}
        {f"- Return Date: {booking.return_date.strftime('%B %d, %Y')}" if booking.return_date else ""}
        {f"- Return Time: {booking.return_time.strftime('%I:%M %p')}" if booking.return_time else ""}

        Your driver will arrive at the pickup location on time. Please ensure you are ready at the scheduled time.

        Payment Information:
        - Payment Method: {booking.payment_type}
        - Payment Status: {booking.payment_status}

        The booking is now fully confirmed and operationally ready.
        If any reassignment, validation, or adjustments are required, please log in to the admin dashboard:

        👉 https://firstclasstransfers.eu/admin/login

        All booking, driver, and vehicle management actions can be handled directly from the dashboard.

        Best regards,
        First Class Transfer Team
    """.strip()

    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [settings.EMAIL_FROM],
            fail_silently=False,
        )
        return True

    return False


def send_status_change_to_admin(user, booking, old_status, new_status):
    """
    Send email to admin notifying them that their booking status has changed.
    """
    passenger = booking.passenger_information
    route = booking.route

    if not passenger or not passenger.email_address:
        return False

    subject = f"Booking {new_status} - #{booking.booking_id}"

    message = f"""
        Hello,

        This is to notify you that the status of a booking on the First Class Transfer platform has been updated.

        Booking Details:
        - Booking ID: {booking.booking_id}
        - Route: {route.from_location} → {route.to_location}
        - Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}
        - Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}
        - Previous Status: {old_status}
        - New Status: {new_status}
        - Changed by : {user.full_name}

        The passenger has been notified of this status change.

        Please review the booking to confirm that the updated status aligns with operational and business requirements.
        If any follow-up actions, corrections, or validations are required, log in to the admin dashboard using the link below:

        👉 https://firstclasstransfers.eu/admin/login

        All booking status management and related actions can be handled directly from the dashboard.

        Best regards,
        First Class Transfer Team
            """.strip()

    with suppress(Exception):
        send_mail(
            subject,
            message,
            settings.EMAIL_FROM,
            [settings.EMAIL_FROM],
            fail_silently=False,
        )
        return True

    return False