from rest_framework import serializers
from .models import DriverNotification


class DriverNotificationSerializer(serializers.ModelSerializer):
    booking_id = serializers.CharField(source='booking.booking_id', read_only=True, allow_null=True)

    class Meta:
        model = DriverNotification
        fields = [
            'id',
            'notification_type',
            'title',
            'message',
            'booking_id',
            'read',
            'created_at',
        ]
        read_only_fields = ['id', 'notification_type', 'title', 'message', 'booking_id', 'created_at']


class DriverNotificationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for notification list."""
    booking_id = serializers.CharField(source='booking.booking_id', read_only=True, allow_null=True)

    class Meta:
        model = DriverNotification
        fields = [
            'id',
            'notification_type',
            'title',
            'booking_id',
            'read',
            'created_at',
        ]


class MarkNotificationReadSerializer(serializers.Serializer):
    """Serializer for marking notifications as read."""
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="List of notification IDs to mark as read. If empty, marks all as read."
    )
