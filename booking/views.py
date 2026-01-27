from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Booking
from .serializers import (
    BookingCreateSerializer,
    BookingListSerializer,
    BookingDetailSerializer,
    AssignDriverSerializer,
    AssignVehicleSerializer,
    AvailableDriverSerializer,
    AvailableVehicleSerializer,
    BookingUpdateSerializer,
)
from .filters import BookingFilter
from .utils import get_available_drivers, get_available_vehicles
from .emails import (
    send_driver_assigned_to_passenger,
    send_booking_assigned_to_driver,
    send_vehicle_assigned_to_passenger,
    send_booking_updated_to_passenger,
    send_booking_updated_to_driver,
)
from notifications.utils import (
    create_booking_assigned_notification,
    create_booking_updated_notification,
    create_booking_status_notification,
    create_vehicle_assigned_notification,
)


class BookingCreateView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = [AllowAny]


class BookingListView(ListAPIView):
    queryset = Booking.objects.select_related(
        'passenger_information',
        'route',
        'vehicle',
        'driver'
    ).order_by('-pickup_date', '-pickup_time')
    serializer_class = BookingListSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookingFilter


class BookingDetailView(RetrieveAPIView):
    serializer_class = BookingDetailSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'booking_id'
    lookup_url_kwarg = 'booking_id'
    queryset = Booking.objects.all()


class BookingUpdateView(UpdateAPIView):
    """
    Update booking details (reschedule, change status, etc.)
    Sends email notifications to passenger and driver about the changes.
    """
    serializer_class = BookingUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'booking_id'
    lookup_url_kwarg = 'booking_id'
    queryset = Booking.objects.select_related(
        'passenger_information',
        'transfer_information',
        'route',
        'vehicle',
        'driver'
    )

    def perform_update(self, serializer):
        # Store old status before update
        old_status = serializer.instance.status if serializer.instance else None

        booking = serializer.save()
        changes = getattr(serializer, 'changes', [])

        # Only send emails and notifications if there were actual changes
        if changes:
            # Send email to passenger
            send_booking_updated_to_passenger(booking, changes)

            # Send email and notification to driver if one is assigned
            if booking.driver:
                send_booking_updated_to_driver(booking, changes)

                # Check if status changed - create specific status notification
                new_status = booking.status
                if old_status and old_status != new_status:
                    create_booking_status_notification(booking, old_status, new_status)
                else:
                    # General update notification
                    create_booking_updated_notification(booking, changes)


class AssignDriverView(UpdateAPIView):
    serializer_class = AssignDriverSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'booking_id'
    lookup_url_kwarg = 'booking_id'
    queryset = Booking.objects.select_related(
        'passenger_information',
        'transfer_information',
        'route',
        'vehicle',
        'driver'
    )

    def perform_update(self, serializer):
        booking = serializer.save()
        # Send email notifications and create driver notification
        if booking.driver:
            send_driver_assigned_to_passenger(booking)
            send_booking_assigned_to_driver(booking)
            create_booking_assigned_notification(booking)


class AssignVehicleView(UpdateAPIView):
    serializer_class = AssignVehicleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'booking_id'
    lookup_url_kwarg = 'booking_id'
    queryset = Booking.objects.select_related(
        'passenger_information',
        'route',
        'vehicle',
        'driver'
    )

    def perform_update(self, serializer):
        booking = serializer.save()
        # Send email notification to passenger
        if booking.vehicle:
            send_vehicle_assigned_to_passenger(booking)
            # Create notification for driver if assigned
            if booking.driver:
                create_vehicle_assigned_notification(booking)


class AvailableDriversView(APIView):
    """
    Get all drivers that are available for a specific booking's time slot.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.select_related('route').get(booking_id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        available_drivers = get_available_drivers(
            booking=booking,
            exclude_booking_id=booking_id
        )

        serializer = AvailableDriverSerializer(available_drivers, many=True)
        return Response(serializer.data)


class AvailableVehiclesView(APIView):
    """
    Get all vehicles that are available for a specific booking's time slot.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, booking_id):
        try:
            booking = Booking.objects.select_related('route').get(booking_id=booking_id)
        except Booking.DoesNotExist:
            return Response(
                {"error": "Booking not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        available_vehicles = get_available_vehicles(
            booking=booking,
            exclude_booking_id=booking_id
        )

        serializer = AvailableVehicleSerializer(available_vehicles, many=True)
        return Response(serializer.data)
