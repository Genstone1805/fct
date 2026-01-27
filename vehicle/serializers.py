from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id','license_plate', 'make', 'model', 'year', 'color', 'type', "max_passengers"]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AvailableVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'year', ]
