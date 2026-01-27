from datetime import datetime, timedelta
from django.db.models import Q


BUFFER_MINUTES = 30


def get_booking_time_windows(booking):
    """
    Calculate the unavailability time windows for a booking.

    Returns a list of tuples: [(start_datetime, end_datetime), ...]
    - One window for one-way trips
    - Two windows for return trips
    """
    windows = []

    route_duration = booking.route.duration_minutes if booking.route else 0
    total_duration = route_duration + BUFFER_MINUTES

    # Window 1: Pickup time window
    if booking.pickup_date and booking.pickup_time:
        pickup_start = datetime.combine(booking.pickup_date, booking.pickup_time)
        pickup_end = pickup_start + timedelta(minutes=total_duration)
        windows.append((pickup_start, pickup_end))

    # Window 2: Return time window (for return trips)
    if booking.trip_type == "Return" and booking.return_date and booking.return_time:
        return_start = datetime.combine(booking.return_date, booking.return_time)
        return_end = return_start + timedelta(minutes=total_duration)
        windows.append((return_start, return_end))

    return windows


def check_time_overlap(window1_start, window1_end, window2_start, window2_end):
    """
    Check if two time windows overlap.
    Returns True if they overlap, False otherwise.
    """
    return window1_start < window2_end and window2_start < window1_end


def get_conflicting_booking_for_driver(driver, booking, exclude_booking_id=None):
    """
    Check if a driver has any conflicting bookings for the given booking's time windows.

    Returns the conflicting booking if found, None otherwise.
    """
    from .models import Booking

    if not driver:
        return None

    # Get time windows for the booking we want to assign
    new_windows = get_booking_time_windows(booking)

    if not new_windows:
        return None

    # Get all non-cancelled bookings for this driver
    existing_bookings = Booking.objects.filter(
        driver=driver
    ).exclude(
        status="Cancelled"
    )

    if exclude_booking_id:
        existing_bookings = existing_bookings.exclude(booking_id=exclude_booking_id)

    # Check each existing booking for conflicts
    for existing_booking in existing_bookings:
        existing_windows = get_booking_time_windows(existing_booking)

        for new_start, new_end in new_windows:
            for existing_start, existing_end in existing_windows:
                if check_time_overlap(new_start, new_end, existing_start, existing_end):
                    return existing_booking

    return None


def get_conflicting_booking_for_vehicle(vehicle, booking, exclude_booking_id=None):
    """
    Check if a vehicle has any conflicting bookings for the given booking's time windows.

    Returns the conflicting booking if found, None otherwise.
    """
    from .models import Booking

    if not vehicle:
        return None

    # Get time windows for the booking we want to assign
    new_windows = get_booking_time_windows(booking)

    if not new_windows:
        return None

    # Get all non-cancelled bookings for this vehicle
    existing_bookings = Booking.objects.filter(
        vehicle=vehicle
    ).exclude(
        status="Cancelled"
    )

    if exclude_booking_id:
        existing_bookings = existing_bookings.exclude(booking_id=exclude_booking_id)

    # Check each existing booking for conflicts
    for existing_booking in existing_bookings:
        existing_windows = get_booking_time_windows(existing_booking)

        for new_start, new_end in new_windows:
            for existing_start, existing_end in existing_windows:
                if check_time_overlap(new_start, new_end, existing_start, existing_end):
                    return existing_booking

    return None


def get_available_drivers(booking, exclude_booking_id=None):
    """
    Get all drivers that are available for the given booking's time windows.

    Returns a queryset of available drivers.
    """
    from account.models import UserProfile
    from .models import Booking

    # Get all active drivers
    all_drivers = UserProfile.objects.filter(is_driver=True, is_active=True, disabled=False)

    # Get time windows for the booking
    new_windows = get_booking_time_windows(booking)

    if not new_windows:
        return all_drivers

    # Find drivers with conflicting bookings
    unavailable_driver_ids = set()

    # Get all non-cancelled bookings with assigned drivers
    existing_bookings = Booking.objects.filter(
        driver__isnull=False
    ).exclude(
        status="Cancelled"
    ).select_related('route', 'driver')

    if exclude_booking_id:
        existing_bookings = existing_bookings.exclude(booking_id=exclude_booking_id)

    for existing_booking in existing_bookings:
        existing_windows = get_booking_time_windows(existing_booking)

        for new_start, new_end in new_windows:
            for existing_start, existing_end in existing_windows:
                if check_time_overlap(new_start, new_end, existing_start, existing_end):
                    unavailable_driver_ids.add(existing_booking.driver_id)
                    break

    return all_drivers.exclude(id__in=unavailable_driver_ids)


def get_available_vehicles(booking, exclude_booking_id=None):
    """
    Get all vehicles that are available for the given booking's time windows.

    Returns a queryset of available vehicles.
    """
    from vehicle.models import Vehicle
    from .models import Booking

    # Get all vehicles
    all_vehicles = Vehicle.objects.all()

    # Get time windows for the booking
    new_windows = get_booking_time_windows(booking)

    if not new_windows:
        return all_vehicles

    # Find vehicles with conflicting bookings
    unavailable_vehicle_ids = set()

    # Get all non-cancelled bookings with assigned vehicles
    existing_bookings = Booking.objects.filter(
        vehicle__isnull=False
    ).exclude(
        status="Cancelled"
    ).select_related('route', 'vehicle')

    if exclude_booking_id:
        existing_bookings = existing_bookings.exclude(booking_id=exclude_booking_id)

    for existing_booking in existing_bookings:
        existing_windows = get_booking_time_windows(existing_booking)

        for new_start, new_end in new_windows:
            for existing_start, existing_end in existing_windows:
                if check_time_overlap(new_start, new_end, existing_start, existing_end):
                    unavailable_vehicle_ids.add(existing_booking.vehicle_id)
                    break

    return all_vehicles.exclude(id__in=unavailable_vehicle_ids)


def format_time_window(start, end):
    """
    Format a time window for display in error messages.
    """
    if start.date() == end.date():
        return f"{start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%H:%M')}"
    return f"{start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%Y-%m-%d %H:%M')}"
