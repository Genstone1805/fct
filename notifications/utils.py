from .models import DriverNotification


def create_booking_assigned_notification(booking):
    """
    Create a notification when a driver is assigned to a booking.
    """
    if not booking.driver:
        return None

    route = booking.route
    title = f"New Booking Assignment - #{booking.booking_id}"
    message = (
        f"You have been assigned to a new booking.\n\n"
        f"Route: {route.from_location} → {route.to_location}\n"
        f"Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}\n"
        f"Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}\n"
        f"Passenger: {booking.passenger_information.full_name}\n"
        f"Phone: {booking.passenger_information.phone_number}"
    )

    if booking.trip_type == "Return" and booking.return_date:
        message += (
            f"\n\nReturn Trip:\n"
            f"Return Date: {booking.return_date.strftime('%B %d, %Y')}\n"
            f"Return Time: {booking.return_time.strftime('%I:%M %p')}"
        )

    return DriverNotification.objects.create(
        driver=booking.driver,
        notification_type='booking_assigned',
        title=title,
        message=message,
        booking=booking
    )


def create_booking_updated_notification(booking, changes=None):
    """
    Create a notification when a booking assigned to a driver is updated.
    """
    if not booking.driver:
        return None

    route = booking.route
    title = f"Booking Updated - #{booking.booking_id}"

    changes_text = ""
    if changes:
        changes_text = "Changes:\n" + "\n".join([f"• {change}" for change in changes]) + "\n\n"

    message = (
        f"A booking you are assigned to has been updated.\n\n"
        f"{changes_text}"
        f"Updated Details:\n"
        f"Route: {route.from_location} → {route.to_location}\n"
        f"Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}\n"
        f"Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}\n"
        f"Status: {booking.booking_status}"
    )

    return DriverNotification.objects.create(
        driver=booking.driver,
        notification_type='booking_updated',
        title=title,
        message=message,
        booking=booking
    )


def create_booking_status_notification(booking, old_status, new_status):
    """
    Create a notification when a booking status changes.
    """
    if not booking.driver:
        return None

    route = booking.route
    title = f"Booking Status Changed - #{booking.booking_id}"
    message = (
        f"The status of your assigned booking has changed.\n\n"
        f"Status: {old_status} → {new_status}\n\n"
        f"Booking Details:\n"
        f"Route: {route.from_location} → {route.to_location}\n"
        f"Pickup Date: {booking.pickup_date.strftime('%B %d, %Y')}\n"
        f"Pickup Time: {booking.pickup_time.strftime('%I:%M %p')}"
    )

    # Determine notification type based on new status
    if new_status == "Completed":
        notification_type = 'booking_completed'
    elif new_status == "Cancelled":
        notification_type = 'booking_cancelled'
    else:
        notification_type = 'booking_updated'

    return DriverNotification.objects.create(
        driver=booking.driver,
        notification_type=notification_type,
        title=title,
        message=message,
        booking=booking
    )


def create_vehicle_assigned_notification(booking):
    """
    Create a notification when a vehicle is assigned to a booking the driver is on.
    """
    if not booking.driver or not booking.vehicle:
        return None

    vehicle = booking.vehicle
    title = f"Vehicle Assigned - #{booking.booking_id}"
    message = (
        f"A vehicle has been assigned to your booking.\n\n"
        f"Vehicle Details:\n"
        f"Type: {vehicle.type}\n"
        f"Make/Model: {vehicle.make} {vehicle.model}\n"
        f"License Plate: {vehicle.license_plate}\n"
        f"Max Passengers: {vehicle.max_passengers}"
    )

    return DriverNotification.objects.create(
        driver=booking.driver,
        notification_type='vehicle_assigned',
        title=title,
        message=message,
        booking=booking
    )


def create_general_notification(driver, title, message, booking=None):
    """
    Create a general notification for a driver.
    """
    return DriverNotification.objects.create(
        driver=driver,
        notification_type='general',
        title=title,
        message=message,
        booking=booking
    )
