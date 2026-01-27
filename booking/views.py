import json

from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from account.permissions import HasBookingPermission

from .models import Booking
from routes.models import Route
from .serializers import (
    BookingCreateSerializer,
    BookingDetailSerializer,
    AssignDriverVehicleSerializer,
    AvailableDriverSerializer,
    AvailableVehicleSerializer,
    BookingUpdateSerializer,
)
from .filters import BookingFilter
from .utils import get_available_drivers, get_available_vehicles
from .emails import (
    send_booking_updated_to_passenger,
    send_booking_updated_to_driver,
    send_assignment_to_passenger,
    send_assignment_to_driver,
)
from notifications.utils import (
    create_booking_assigned_notification,
    create_booking_updated_notification,
    create_booking_status_notification,
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
    serializer_class = BookingDetailSerializer
    permission_classes = [HasBookingPermission]
    filterset_class = BookingFilter

class BookingUpdateView(UpdateAPIView):
    """
    Update booking details (reschedule, change status, etc.)
    Sends email notifications to passenger and driver about the changes.
    """
    serializer_class = BookingUpdateSerializer
    permission_classes = [HasBookingPermission]
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


class AvailableDriversView(APIView):
    """
    Get all drivers that are available for a specific booking's time slot.
    """
    permission_classes = [HasBookingPermission]

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
    permission_classes = [HasBookingPermission]

    def get(self, request):
        from vehicle.models import Vehicle

        vehicle_type = request.query_params.get('vehicle_type')

        if not vehicle_type:
            return Response(
                {"error": "vehicle_type query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        vehicles = Vehicle.objects.filter(type=vehicle_type)

        serializer = AvailableVehicleSerializer(vehicles, many=True)
        return Response(serializer.data)


class AssignDriverVehicleView(UpdateAPIView):
    """
    Assign both driver and vehicle to a booking.
    Accepts driver ID and vehicle ID, validates availability, and assigns them.
    """
    serializer_class = AssignDriverVehicleSerializer
    permission_classes = [HasBookingPermission]
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

        # Update status to Assigned (both driver and vehicle are required)
        booking.status = 'Assigned'
        booking.save(update_fields=['status'])

        # Send email to passenger with driver and vehicle info
        send_assignment_to_passenger(booking)

        # Send email to driver with booking and vehicle info
        send_assignment_to_driver(booking)

        # Create notification for the driver
        create_booking_assigned_notification(booking)
