from rest_framework import serializers
from account.models import UserProfile


class DriverListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'email', 'phone_number', 'dp', 'full_name',
            'license_number', 'status', 'date_joined', 'is_active', 'disabled'
        ]
        read_only_fields = ['id', 'date_joined']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'email', 'phone_number', 'dp', 'full_name',
            'license_number', 'status', 'date_joined', 'is_active', 'disabled'
        ]
        read_only_fields = ['id', 'date_joined', "email"]


class DriverUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'email', 'phone_number', 'dp', 'full_name',
            'license_number', 'status', 'is_active', 'disabled'
        ]

    def validate_email(self, value):
        instance = self.instance
        if instance and UserProfile.objects.filter(email=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_phone_number(self, value):
        instance = self.instance
        if value and instance and UserProfile.objects.filter(phone_number=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        return value


class AvailableDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'full_name']
        read_only_fields = ['id', 'full_name']
