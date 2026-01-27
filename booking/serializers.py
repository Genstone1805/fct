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
        fields = ['route_id', 'from_location', 'to_location', 'distance', 'time']


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
            'vehicle',
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


class AssignVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['vehicle']
