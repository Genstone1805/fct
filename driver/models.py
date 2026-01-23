from django.db import models


class Driver(models.Model):
    STATUS_CHOICES = [
        ("Available", "Available"),
        ("On Trip", "On Trip"),
        ("Off Duty", "Off Duty"),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    license_number = models.CharField(max_length=50, unique=True)
    profile_picture = models.ImageField(upload_to="driver_pictures", blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="Available")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'

    def __str__(self):
        return self.full_name
