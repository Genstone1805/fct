import json

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from admin.views import JSONFieldParserMixin

from .models import Booking
from routes.models import Route
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
from fct.parsers import recursive_underscoreize


class BookingCreateView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = [AllowAny]
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
                    try:
                        parsed = json.loads(data[field])
                        data[field] = recursive_underscoreize(parsed)
                    except (json.JSONDecodeError, TypeError):
                        pass

            # Convert route_id (string) to route pk (integer)
            if 'route' in data and isinstance(data['route'], str):
                try:
                    route_obj = Route.objects.get(route_id=data['route'])
                    data['route'] = route_obj.pk
                except Route.DoesNotExist:
                    pass  # Let serializer handle the validation error

            kwargs['data'] = data

        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mutate data here as needed
        # Example: validated_data = serializer.validated_data
        # validated_data['some_field'] = modified_value

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
