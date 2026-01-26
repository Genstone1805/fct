from rest_framework import serializers
from account.models import UserProfile



class DriverRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['email', 'phone_number', 'dp', 'full_name', "license_number", "is_driver"]

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

class DriverListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'email', 'phone_number', 'dp', 'full_name',
            'license_number', 'date_joined', 'is_active', 'disabled'
        ]
        read_only_fields = ['id', 'date_joined']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'email', 'phone_number', 'dp', 'full_name',
            'license_number', 'date_joined', 'is_active', 'disabled'
        ]
        read_only_fields = ['id', 'date_joined', "email"]

class AvailableDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'full_name']
        read_only_fields = ['id', 'full_name']
