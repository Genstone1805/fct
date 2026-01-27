from django.urls import path

from .views import (
    DriverNotificationListView,
    DriverNotificationDetailView,
    MarkNotificationsReadView,
    UnreadNotificationCountView,
)

urlpatterns = [
    path('driver/', DriverNotificationListView.as_view(), name='driver-notifications'),
    path('driver/<int:id>/', DriverNotificationDetailView.as_view(), name='driver-notification-detail'),
    path('driver/mark-read/', MarkNotificationsReadView.as_view(), name='mark-notifications-read'),
    path('driver/unread-count/', UnreadNotificationCountView.as_view(), name='unread-notification-count'),
]
