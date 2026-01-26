from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'make', 'model', 'year', 'color', 'type']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AvailableVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'year', ]
