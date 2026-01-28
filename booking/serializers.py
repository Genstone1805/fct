from rest_framework import serializers

from .models import Booking, TransferInformation, PassengerDetail
from routes.models import Route
from vehicle.models import Vehicle
from account.models import UserProfile


class TransferInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferInformation
        fields = ['flight_number', 'adults', 'children', 'luggage']


class PassengerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetail
        fields = ['full_name', 'phone_number', 'email_address', 'additional_information']


# Nested serializers for list view
class PassengerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetail
        fields = ['full_name', 'email_address']


class RouteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['from_location', 'to_location']


class VehicleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'make', 'model', 'type']


class DriverListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name']


class AvailableDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'full_name']


class AvailableVehicleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Vehicle
        fields = ['id', 'name']

    def get_name(self, obj):
        parts = [obj.make, obj.model]
        if obj.year:
            parts.append(obj.year)
        if obj.color:
            parts.append(obj.color)
        return ' '.join(parts)


class BookingListSerializer(serializers.ModelSerializer):
    passenger_information = PassengerListSerializer(read_only=True)
    route = RouteListSerializer(read_only=True)
    vehicle = VehicleListSerializer(read_only=True)
    driver = DriverListSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'passenger_information',
            'route',
            'pickup_date',
            'pickup_time',
            'payment_type',
            'payment_id',
            'vehicle',
            'driver',
            'payment_status',
        ]


# Nested serializers for detail view
class RouteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['route_id', 'from_location', 'to_location', 'distance', 'time', 'duration_minutes']


class VehicleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'make', 'model', 'type', 'max_passengers']


class DriverDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'phone_number']


class BookingDetailSerializer(serializers.ModelSerializer):
    transfer_information = TransferInformationSerializer(read_only=True)
    passenger_information = PassengerDetailSerializer(read_only=True)
    route = RouteDetailSerializer(read_only=True)
    vehicle = VehicleDetailSerializer(read_only=True)
    driver = DriverDetailSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'booking_id',
            'route',
            'vehicle',
            "price",
            "vehicle_type",
            'driver',
            'payment_type',
            'payment_status',
            'payment_id',
            'trip_type',
            'pickup_date',
            'pickup_time',
            'time_period',
            'return_date',
            'return_time',
            'transfer_information',
            'passenger_information',
        ]


class BookingCreateSerializer(serializers.ModelSerializer):
    transfer_information = TransferInformationSerializer()
    passenger_information = PassengerDetailSerializer()

    class Meta:
        model = Booking
        fields = [
            'route',
            "price",
            "vehicle_type",
            'payment_type',
            'trip_type',
            'pickup_date',
            'pickup_time',
            'time_period',
            'return_date',
            'return_time',
            'transfer_information',
            'passenger_information',
        ]


    def create(self, validated_data):
        transfer_data = validated_data.pop('transfer_information')
        passenger_data = validated_data.pop('passenger_information')

        transfer_info = TransferInformation.objects.create(**transfer_data)
        passenger_info = PassengerDetail.objects.create(**passenger_data)

        booking = Booking.objects.create(
            transfer_information=transfer_info,
            passenger_information=passenger_info,
            **validated_data
        )

        return booking

    def validate(self, data):
        if data.get('trip_type') == 'Return':
            if not data.get('return_date') or not data.get('return_time'):
                raise serializers.ValidationError(
                    "Return date and time are required for return trips."
                )
        return data


class AssignDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['driver']

    def validate_driver(self, value):
        from .utils import (
            get_conflicting_booking_for_driver,
            get_booking_time_windows,
            format_time_window,
        )

        if not value:
            return value

        booking = self.instance

        # Check for conflicting bookings
        conflicting_booking = get_conflicting_booking_for_driver(
            driver=value,
            booking=booking,
            exclude_booking_id=booking.booking_id if booking else None
        )

        if conflicting_booking:
            windows = get_booking_time_windows(conflicting_booking)
            window_str = ", ".join([format_time_window(s, e) for s, e in windows])
            raise serializers.ValidationError(
                f"Driver '{value.full_name}' is unavailable. "
                f"Already assigned to booking #{conflicting_booking.booking_id} "
                f"({window_str})."
            )

        return value


class AssignVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['vehicle']

    def validate_vehicle(self, value):
        from .utils import (
            get_conflicting_booking_for_vehicle,
            get_booking_time_windows,
            format_time_window,
        )

        if not value:
            return value

        booking = self.instance

        # Check for conflicting bookings
        conflicting_booking = get_conflicting_booking_for_vehicle(
            vehicle=value,
            booking=booking,
            exclude_booking_id=booking.booking_id if booking else None
        )

        if conflicting_booking:
            windows = get_booking_time_windows(conflicting_booking)
            window_str = ", ".join([format_time_window(s, e) for s, e in windows])
            raise serializers.ValidationError(
                f"Vehicle '{value}' is unavailable. "
                f"Already assigned to booking #{conflicting_booking.booking_id} "
                f"({window_str})."
            )

        return value


class AssignDriverVehicleSerializer(serializers.ModelSerializer):
    """Serializer for assigning both driver and vehicle to a booking."""
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.filter(is_driver=True),
        source='driver',
        required=True,
        allow_null=False
    )
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        source='vehicle',
        required=True,
        allow_null=False
    )

    class Meta:
        model = Booking
        fields = ['driver_id', 'vehicle_id']

    def validate_driver_id(self, value):
        from .utils import (
            get_conflicting_booking_for_driver,
            get_booking_time_windows,
            format_time_window,
        )

        if not value:
            raise serializers.ValidationError("Driver is required.")

        booking = self.instance

        conflicting_booking = get_conflicting_booking_for_driver(
            driver=value,
            booking=booking,
            exclude_booking_id=booking.booking_id if booking else None
        )

        if conflicting_booking:
            windows = get_booking_time_windows(conflicting_booking)
            window_str = ", ".join([format_time_window(s, e) for s, e in windows])
            raise serializers.ValidationError(
                f"Driver '{value.full_name}' is unavailable. "
                f"Already assigned to booking #{conflicting_booking.booking_id} "
                f"({window_str})."
            )

        return value

    def validate_vehicle_id(self, value):
        from .utils import (
            get_conflicting_booking_for_vehicle,
            get_booking_time_windows,
            format_time_window,
        )

        if not value:
            raise serializers.ValidationError("Vehicle is required.")

        booking = self.instance

        conflicting_booking = get_conflicting_booking_for_vehicle(
            vehicle=value,
            booking=booking,
            exclude_booking_id=booking.booking_id if booking else None
        )

        if conflicting_booking:
            windows = get_booking_time_windows(conflicting_booking)
            window_str = ", ".join([format_time_window(s, e) for s, e in windows])
            raise serializers.ValidationError(
                f"Vehicle '{value}' is unavailable. "
                f"Already assigned to booking #{conflicting_booking.booking_id} "
                f"({window_str})."
            )

        return value

    def update(self, instance, validated_data):
        instance.driver = validated_data.get('driver', instance.driver)
        instance.vehicle = validated_data.get('vehicle', instance.vehicle)
        instance.save(update_fields=['driver', 'vehicle'])
        return instance


class BookingStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating booking status to Completed or Cancelled."""
    ALLOWED_STATUSES = ['Completed', 'Cancelled']

    class Meta:
        model = Booking
        fields = ['status']

    def validate_status(self, value):
        if not value:
            raise serializers.ValidationError("Status is required.")
        if value not in self.ALLOWED_STATUSES:
            raise serializers.ValidationError(
                f"Invalid status. Allowed values: {', '.join(self.ALLOWED_STATUSES)}"
            )
        return value

    def update(self, instance, validated_data):
        self.old_status = instance.status
        new_status = validated_data['status']

        # Use direct database update to ensure it's saved
        Booking.objects.filter(pk=instance.pk).update(status=new_status)

        # Update the instance in memory
        instance.status = new_status
        return instance


class RescheduleBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for rescheduling a booking's pickup and return dates/times.
    Validates driver and vehicle availability for new times.
    All fields are optional - only provided fields will be updated.
    """
    class Meta:
        model = Booking
        fields = ['pickup_date', 'pickup_time', 'return_date', 'return_time']
        extra_kwargs = {
            'pickup_date': {'required': False},
            'pickup_time': {'required': False},
            'return_date': {'required': False},
            'return_time': {'required': False},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self._original_values = {
                'pickup_date': self.instance.pickup_date,
                'pickup_time': self.instance.pickup_time,
                'return_date': self.instance.return_date,
                'return_time': self.instance.return_time,
            }
        else:
            self._original_values = {}

    def get_changes(self, validated_data):
        """Compare original values with new values and return list of changes."""
        changes = []
        field_labels = {
            'pickup_date': 'Pickup Date',
            'pickup_time': 'Pickup Time',
            'return_date': 'Return Date',
            'return_time': 'Return Time',
        }

        for field, label in field_labels.items():
            if field in validated_data:
                old_value = self._original_values.get(field)
                new_value = validated_data[field]

                if old_value != new_value:
                    if field in ['pickup_date', 'return_date']:
                        old_str = old_value.strftime('%B %d, %Y') if old_value else 'Not set'
                        new_str = new_value.strftime('%B %d, %Y') if new_value else 'Not set'
                    else:
                        old_str = old_value.strftime('%I:%M %p') if old_value else 'Not set'
                        new_str = new_value.strftime('%I:%M %p') if new_value else 'Not set'

                    changes.append(f"{label}: {old_str} → {new_str}")

        return changes

    def validate(self, data):
        from .utils import (
            get_conflicting_booking_for_driver,
            get_conflicting_booking_for_vehicle,
            get_booking_time_windows,
            format_time_window,
        )

        instance = self.instance
        if not instance:
            raise serializers.ValidationError("Booking instance is required.")

        # Check if return trip requires return date/time
        trip_type = instance.trip_type
        if trip_type == 'Return':
            return_date = data.get('return_date', instance.return_date)
            return_time = data.get('return_time', instance.return_time)
            if not return_date or not return_time:
                raise serializers.ValidationError(
                    "Return date and time are required for return trips."
                )

        # Create a temporary booking object with new values to check availability
        temp_booking = Booking(
            id=instance.id,
            booking_id=instance.booking_id,
            route=instance.route,
            pickup_date=data.get('pickup_date', instance.pickup_date),
            pickup_time=data.get('pickup_time', instance.pickup_time),
            return_date=data.get('return_date', instance.return_date),
            return_time=data.get('return_time', instance.return_time),
            trip_type=instance.trip_type,
        )

        # Check driver availability with new times
        if instance.driver:
            conflicting = get_conflicting_booking_for_driver(
                driver=instance.driver,
                booking=temp_booking,
                exclude_booking_id=instance.booking_id
            )
            if conflicting:
                windows = get_booking_time_windows(conflicting)
                window_str = ", ".join([format_time_window(s, e) for s, e in windows])
                raise serializers.ValidationError(
                    f"Cannot reschedule: Driver '{instance.driver.full_name}' "
                    f"has a conflicting booking #{conflicting.booking_id} ({window_str}). "
                    f"Please reassign the driver first or choose a different time."
                )

        # Check vehicle availability with new times
        if instance.vehicle:
            conflicting = get_conflicting_booking_for_vehicle(
                vehicle=instance.vehicle,
                booking=temp_booking,
                exclude_booking_id=instance.booking_id
            )
            if conflicting:
                windows = get_booking_time_windows(conflicting)
                window_str = ", ".join([format_time_window(s, e) for s, e in windows])
                raise serializers.ValidationError(
                    f"Cannot reschedule: Vehicle '{instance.vehicle}' "
                    f"has a conflicting booking #{conflicting.booking_id} ({window_str}). "
                    f"Please reassign the vehicle first or choose a different time."
                )

        return data

    def update(self, instance, validated_data):
        self.changes = self.get_changes(validated_data)

        instance.pickup_date = validated_data.get('pickup_date', instance.pickup_date)
        instance.pickup_time = validated_data.get('pickup_time', instance.pickup_time)
        instance.return_date = validated_data.get('return_date', instance.return_date)
        instance.return_time = validated_data.get('return_time', instance.return_time)
        instance.save(update_fields=['pickup_date', 'pickup_time', 'return_date', 'return_time'])

        return instance


class BookingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating booking details.
    Tracks changes for email notifications.
    """
    class Meta:
        model = Booking
        fields = [
            'status',
            'pickup_date',
            'pickup_time',
            'return_date',
            'return_time',
            'trip_type',
            'time_period',
            'payment_status',
            'payment_type',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store original values for change tracking
        if self.instance:
            self._original_values = {
                'status': self.instance.status,
                'pickup_date': self.instance.pickup_date,
                'pickup_time': self.instance.pickup_time,
                'return_date': self.instance.return_date,
                'return_time': self.instance.return_time,
                'trip_type': self.instance.trip_type,
                'time_period': self.instance.time_period,
                'payment_status': self.instance.payment_status,
                'payment_type': self.instance.payment_type,
            }
        else:
            self._original_values = {}

    def get_changes(self, validated_data):
        """
        Compare original values with new values and return list of changes.
        """
        changes = []
        field_labels = {
            'status': 'Status',
            'pickup_date': 'Pickup Date',
            'pickup_time': 'Pickup Time',
            'return_date': 'Return Date',
            'return_time': 'Return Time',
            'trip_type': 'Trip Type',
            'time_period': 'Time Period',
            'payment_status': 'Payment Status',
            'payment_type': 'Payment Type',
        }

        for field, label in field_labels.items():
            if field in validated_data:
                old_value = self._original_values.get(field)
                new_value = validated_data[field]

                if old_value != new_value:
                    # Format dates and times nicely
                    if field in ['pickup_date', 'return_date'] and new_value:
                        old_str = old_value.strftime('%B %d, %Y') if old_value else 'Not set'
                        new_str = new_value.strftime('%B %d, %Y') if new_value else 'Not set'
                    elif field in ['pickup_time', 'return_time'] and new_value:
                        old_str = old_value.strftime('%I:%M %p') if old_value else 'Not set'
                        new_str = new_value.strftime('%I:%M %p') if new_value else 'Not set'
                    else:
                        old_str = str(old_value) if old_value else 'Not set'
                        new_str = str(new_value) if new_value else 'Not set'

                    changes.append(f"{label}: {old_str} → {new_str}")

        return changes

    def validate(self, data):
        from .utils import (
            get_conflicting_booking_for_driver,
            get_conflicting_booking_for_vehicle,
            get_booking_time_windows,
            format_time_window,
        )

        # If pickup time or date is changing, validate driver/vehicle availability
        time_changed = (
            'pickup_date' in data and data['pickup_date'] != self._original_values.get('pickup_date') or
            'pickup_time' in data and data['pickup_time'] != self._original_values.get('pickup_time') or
            'return_date' in data and data['return_date'] != self._original_values.get('return_date') or
            'return_time' in data and data['return_time'] != self._original_values.get('return_time')
        )

        if time_changed and self.instance:
            # Create a temporary booking-like object with new values to check availability
            temp_booking = Booking(
                id=self.instance.id,
                booking_id=self.instance.booking_id,
                route=self.instance.route,
                pickup_date=data.get('pickup_date', self.instance.pickup_date),
                pickup_time=data.get('pickup_time', self.instance.pickup_time),
                return_date=data.get('return_date', self.instance.return_date),
                return_time=data.get('return_time', self.instance.return_time),
                trip_type=data.get('trip_type', self.instance.trip_type),
            )

            # Check driver availability with new times
            if self.instance.driver:
                conflicting = get_conflicting_booking_for_driver(
                    driver=self.instance.driver,
                    booking=temp_booking,
                    exclude_booking_id=self.instance.booking_id
                )
                if conflicting:
                    windows = get_booking_time_windows(conflicting)
                    window_str = ", ".join([format_time_window(s, e) for s, e in windows])
                    raise serializers.ValidationError(
                        f"Cannot reschedule: Driver '{self.instance.driver.full_name}' "
                        f"has a conflicting booking #{conflicting.booking_id} ({window_str}). "
                        f"Please reassign the driver first or choose a different time."
                    )

            # Check vehicle availability with new times
            if self.instance.vehicle:
                conflicting = get_conflicting_booking_for_vehicle(
                    vehicle=self.instance.vehicle,
                    booking=temp_booking,
                    exclude_booking_id=self.instance.booking_id
                )
                if conflicting:
                    windows = get_booking_time_windows(conflicting)
                    window_str = ", ".join([format_time_window(s, e) for s, e in windows])
                    raise serializers.ValidationError(
                        f"Cannot reschedule: Vehicle '{self.instance.vehicle}' "
                        f"has a conflicting booking #{conflicting.booking_id} ({window_str}). "
                        f"Please reassign the vehicle first or choose a different time."
                    )

        # Validate return trip requirements
        trip_type = data.get('trip_type', self.instance.trip_type if self.instance else None)
        if trip_type == 'Return':
            return_date = data.get('return_date', self.instance.return_date if self.instance else None)
            return_time = data.get('return_time', self.instance.return_time if self.instance else None)
            if not return_date or not return_time:
                raise serializers.ValidationError(
                    "Return date and time are required for return trips."
                )

        return data

    def update(self, instance, validated_data):
        # Store changes before update
        self.changes = self.get_changes(validated_data)
        return super().update(instance, validated_data)
