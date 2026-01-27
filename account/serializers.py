from rest_framework import serializers
from .models import UserProfile
import json


VALID_PERMISSIONS = ['booking', 'drivers', 'routes', 'vehicles', 'adminUsers']


class SignUpSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.ChoiceField(choices=VALID_PERMISSIONS),
        required=False,
        default=list
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'phone_number', 'dp', 'full_name', 'permissions']

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_permissions(self, value):
        for perm in value:
            if perm not in VALID_PERMISSIONS:
                raise serializers.ValidationError(f"Invalid permission: {perm}")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'phone_number', 'dp', 'full_name', 'date_joined', 'user_permissions', 'is_staff', 'disabled', 'added_by']
        read_only_fields = ['id', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(
        child=serializers.ChoiceField(choices=VALID_PERMISSIONS),
        required=False,
        source='user_permissions'
    )

    class Meta:
        model = UserProfile
        fields = ['email', 'phone_number', 'dp', 'full_name', 'permissions', 'is_staff', 'disabled']
        read_only_fields = ["email"]

    def validate_email(self, value):
        instance = self.instance
        if instance and UserProfile.objects.filter(email=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate_permissions(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError("Invalid permissions format")

        if not isinstance(value, list):
            raise serializers.ValidationError("Permissions must be a list")

        return value
