from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ("Sedan", "Sedan"),
        ("Minivan", "Minivan"),
    ]


    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # Basic vehicle info
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.CharField(max_length=4, null=True, blank=True)
    color = models.CharField(max_length=30, null=True, blank=True)
    type = models.CharField(choices=VEHICLE_TYPE_CHOICES, max_length=20, default="Sedan")

    # Capacity
    max_passengers = models.PositiveIntegerField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.make} {self.model} ({self.type})"


