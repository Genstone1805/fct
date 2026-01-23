from rest_framework import serializers

from .models import Booking, TransferInformation, PassengerDetail


class TransferInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferInformation
        fields = ['flight_number', 'adults', 'children', 'luggage']


class PassengerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetail
        fields = ['full_name', 'phone_number', 'email_address', 'additional_information']


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
            status='Pending',
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
