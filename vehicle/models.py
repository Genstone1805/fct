from django.db import models


class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ("Sedan", "Sedan"),
        ("Minivan", "Minivan"),
    ]

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Unavailable", "Unavailable"),
    ]

    # Status
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="Available")
    
    # Basic vehicle info
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField(null=True, blank=True)
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


