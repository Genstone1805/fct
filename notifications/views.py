from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import DriverNotification
from .serializers import (
    DriverNotificationSerializer,
    DriverNotificationListSerializer,
    MarkNotificationReadSerializer,
)


class DriverNotificationListView(ListAPIView):
    """
    List all notifications for the authenticated driver.
    Supports filtering by read status via query param: ?read=true or ?read=false
    """
    serializer_class = DriverNotificationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = DriverNotification.objects.filter(driver=user)

        # Filter by read status if provided
        read_param = self.request.query_params.get('read')
        if read_param is not None:
            if read_param.lower() == 'true':
                queryset = queryset.filter(read=True)
            elif read_param.lower() == 'false':
                queryset = queryset.filter(read=False)

        return queryset


class DriverNotificationDetailView(RetrieveAPIView):
    """
    Get a single notification detail.
    Automatically marks the notification as read when viewed.
    """
    serializer_class = DriverNotificationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return DriverNotification.objects.filter(driver=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Mark as read when viewed
        instance.mark_as_read()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MarkNotificationsReadView(APIView):
    """
    Mark notifications as read.
    - POST with empty body or {"notification_ids": []} marks ALL unread notifications as read
    - POST with {"notification_ids": [1, 2, 3]} marks specific notifications as read
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MarkNotificationReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notification_ids = serializer.validated_data.get('notification_ids', [])

        queryset = DriverNotification.objects.filter(
            driver=request.user,
            read=False
        )

        if notification_ids:
            queryset = queryset.filter(id__in=notification_ids)

        count = queryset.update(read=True)

        return Response({
            'message': f'{count} notification(s) marked as read',
            'count': count
        })


class UnreadNotificationCountView(APIView):
    """
    Get the count of unread notifications for the authenticated driver.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = DriverNotification.objects.filter(
            driver=request.user,
            read=False
        ).count()

        return Response({
            'unread_count': count
        })
