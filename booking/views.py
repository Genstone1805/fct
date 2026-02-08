import json

from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from account.permissions import HasBookingPermission, HasRoutesAPIKey, IsDriverPermission
from rest_framework.generics import ListAPIView
from fct.utils import CustomPagination
from account.utils import log_user_activity

from .models import Booking
from routes.models import Route
from .serializers import (
    BookingCreateSerializer,
    BookingDetailSerializer,
    AssignDriverVehicleSerializer,
    AvailableDriverSerializer,
    AvailableVehicleSerializer,
    BookingUpdateSerializer,
    BookingStatusSerializer,
    RescheduleBookingSerializer,
    BookingStateSerializer
)
from .filters import BookingFilter
from .utils import get_available_drivers, get_available_vehicles
from .emails import (
    send_booking_confirmation_to_passenger,
    send_booking_updated_to_passenger,
    send_booking_updated_to_driver,
    send_assignment_to_passenger,
    send_assignment_to_driver,
    send_status_change_to_passenger,
    send_status_change_to_driver,
    send_payment_status_update_to_passenger,
)
from notifications.utils import (
    create_booking_assigned_notification,
    create_booking_updated_notification,
    create_booking_status_notification,
)
from fct.parsers import recursive_underscoreize
from contextlib import suppress


class BookingCreateView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = [HasRoutesAPIKey]
    parser_classes = [MultiPartParser, FormParser]

    json_fields = ['transfer_information', 'passenger_information']

    def get_serializer(self, *args, **kwargs):
        """Parse JSON fields from multipart form data and convert route_id to pk."""
        if 'data' in kwargs:
            raw_data = kwargs['data']
            if hasattr(raw_data, 'dict'):
                data: dict = raw_data.dict()
            else:
                data: dict = dict(raw_data)

            # Convert camelCase keys to snake_case for all top-level fields
            data = dict(recursive_underscoreize(data))

            # Parse JSON string fields (now using snake_case keys)
            for field in self.json_fields:
                if field in data and isinstance(data[field], str):
                    with suppress(Exception):
                        parsed = json.loads(data[field])
                        data[field] = recursive_underscoreize(parsed)


            # Convert route_id (string) to route pk (integer)
            if 'route' in data and isinstance(data['route'], str):
                with suppress(Exception):
                    route_obj = Route.objects.get(route_id=data['route'])
                    data['route'] = route_obj.pk
# Let serializer handle the validation error

            kwargs['data'] = data

        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = serializer.save()

        return Response(
            {"message": "Booking created successfully", "booking_id": booking.booking_id},
            status=status.HTTP_201_CREATED
        )
        
    


class BookingListView(ListAPIView):
    queryset = Booking.objects.select_related(
        'passenger_information',
        'route',
        'vehicle',
        'driver'
    ).order_by('-pickup_date', '-pickup_time')
    serializer_class = BookingDetailSerializer
    permission_classes = [HasRoutesAPIKey, HasBookingPermission]
    filterset_class = BookingFilter

class BookingUpdateView(UpdateAPIView):
    """
    Update booking details (reschedule, change status, etc.)
    Sends email notifications to passenger and driver about the changes.
    """
    serializer_class = BookingUpdateSerializer
    permission_classes = [HasRoutesAPIKey, HasBookingPermission]
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
        old_status = serializer.instance.booking_status if serializer.instance else None

        booking = serializer.save()

        # Log user activity
        user = self.request.user
        log_user_activity(
            user,
            f"Updated Booking: {booking.route.from_location} → {booking.route.to_location} ({booking.booking_id})",
            self.request
        )

        changes = getattr(serializer, 'changes', [])

        # Only send emails and notifications if there were actual changes
        
        if changes:
            # Send email to passenger
            send_booking_updated_to_passenger(booking, changes)

            # Send email and notification to driver if one is assigned
            if booking.driver:
                send_booking_updated_to_driver(booking, changes)

                # Check if status changed - create specific status notification
                new_status = booking.booking_status
                if old_status and old_status != new_status:
                    create_booking_status_notification(booking, old_status, new_status)
                else:
                    # General update notification
                    create_booking_updated_notification(booking, changes)


class AvailableDriversView(APIView):
    """
    Get all drivers that are available for a specific booking's time slot.
    """
    permission_classes = [HasRoutesAPIKey, HasBookingPermission]

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
    permission_classes = [HasRoutesAPIKey, HasBookingPermission]

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

        vehicle_type = request.query_params.get('vehicle_type')
        if vehicle_type:
            available_vehicles = available_vehicles.filter(type=vehicle_type)

        serializer = AvailableVehicleSerializer(available_vehicles, many=True)
        return Response(serializer.data)


class AssignDriverVehicleView(UpdateAPIView):
    """
    Assign both driver and vehicle to a booking.
    Accepts driver ID and vehicle ID, validates availability, and assigns them.
    """
    serializer_class = AssignDriverVehicleSerializer
    permission_classes = [HasRoutesAPIKey, HasBookingPermission]
    lookup_field = 'booking_id'
    lookup_url_kwarg = 'booking_id'
    queryset = Booking.objects.select_related(
        'passenger_information',
        'transfer_information',
        'route',
        'vehicle',
        'driver'
    )
    
    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        serializer = self.get_serializer(instance=booking, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_update(serializer)
        return Response(
            {'message': 'Driver and vehicle assigned successfully'},
            status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        booking = serializer.save()

        # Update status to Assigned (both driver and vehicle are required)
        booking.booking_status = 'Assigned'
        booking.save(update_fields=['booking_status'])

        # Log user activity
        log_user_activity(
            self.request.user,
            f"Assigned Driver/Vehicle: {booking.driver.full_name} & {booking.vehicle.license_plate} to {booking.booking_id}",
            self.request
        )

        # Send email to passenger with driver and vehicle info
        send_assignment_to_passenger(booking)

        # Send email to driver with booking and vehicle info
        send_assignment_to_driver(booking)

        # Create notification for the driver
        create_booking_assigned_notification(booking)


class BookingStatusUpdateView(UpdateAPIView):
    """
    Update booking status to Completed or Cancelled.
    """
    serializer_class = BookingStatusSerializer
    permission_classes = [HasRoutesAPIKey, HasBookingPermission]
    lookup_field = 'booking_id'
    lookup_url_kwarg = 'booking_id'
    queryset = Booking.objects.select_related(
        'driver', 'passenger_information', 'route'
    )

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        old_status = booking.booking_status

        serializer = self.get_serializer(instance=booking, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = serializer.save()
        new_status = booking.booking_status

        # Log user activity
        log_user_activity(
            request.user,
            f"Changed Booking Status: {booking.booking_id} from {old_status} to {new_status}",
            request
        )

        # Send email to passenger about status change
        send_status_change_to_passenger(booking, old_status, new_status)

        # Send email and notification to driver if assigned
        if booking.driver:
            send_status_change_to_driver(booking, old_status, new_status)
            create_booking_status_notification(booking, old_status, new_status)

        return Response(
            {'message': f'Booking status updated to {new_status}'},
            status=status.HTTP_200_OK
        )


class RescheduleBookingView(UpdateAPIView):
    """
    Reschedule a booking's pickup and return dates/times.
    Validates driver and vehicle availability for new times.
    """
    serializer_class = RescheduleBookingSerializer
    permission_classes = [HasRoutesAPIKey, HasBookingPermission]
    lookup_field = 'booking_id'
    lookup_url_kwarg = 'booking_id'
    queryset = Booking.objects.select_related(
        'driver', 'vehicle', 'passenger_information', 'route'
    )

    def update(self, request, *args, **kwargs):
        booking = self.get_object()
        serializer = self.get_serializer(instance=booking, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        changes = getattr(serializer, 'changes', [])

        # Log user activity
        log_user_activity(
            request.user,
            f"Rescheduled Booking: {booking.booking_id} ({booking.route.from_location} → {booking.route.to_location})",
            request
        )

        # Send emails and notifications if there were changes
        if changes:
            send_booking_updated_to_passenger(booking, changes)

            if booking.driver:
                send_booking_updated_to_driver(booking, changes)
                create_booking_updated_notification(booking, changes)

        return Response(
            {'message': 'Booking rescheduled successfully', 'changes': changes},
            status=status.HTTP_200_OK
        )

class UserBookingsView(ListAPIView):
    serializer_class = BookingDetailSerializer
    permission_classes = [HasRoutesAPIKey, IsDriverPermission ]
    filterset_class = BookingFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        if not user_id:
            return Booking.objects.none()

        return Booking.objects.filter(
            driver__pk=user_id
        ).select_related(
            'passenger_information',
            'route',
            'vehicle',
            'driver'
        ).order_by('-pickup_date', '-pickup_time')

class UpdateBookingStatusView(RetrieveUpdateAPIView):
    serializer_class = BookingStateSerializer
    permission_classes = [HasRoutesAPIKey]
    lookup_field = "transaction_id"
    queryset = Booking.objects.all()

    def perform_update(self, serializer):
        old_status = serializer.instance.payment_status
        booking = serializer.save()
        new_status = booking.payment_status
        if old_status != new_status:
            send_payment_status_update_to_passenger(booking, old_status, new_status)