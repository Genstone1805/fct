from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class DriverNotification(models.Model):
    """
    Notification model for drivers.
    Stores notifications related to bookings and driver activities.
    """
    NOTIFICATION_TYPES = [
        ('booking_assigned', 'Booking Assigned'),
        ('booking_updated', 'Booking Updated'),
        ('booking_completed', 'Booking Completed'),
        ('booking_cancelled', 'Booking Cancelled'),
        ('vehicle_assigned', 'Vehicle Assigned'),
        ('schedule_change', 'Schedule Change'),
        ('general', 'General'),
    ]

    driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        limit_choices_to={'is_driver': True}
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='general'
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    booking = models.ForeignKey(
        'booking.Booking',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='driver_notifications'
    )
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Driver Notification'
        verbose_name_plural = 'Driver Notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.driver.full_name}"

    def mark_as_read(self):
        """Mark the notification as read."""
        if not self.read:
            self.read = True
            self.save(update_fields=['read'])
