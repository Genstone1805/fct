from django.db import models


class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ("Sedan", "Sedan"),
        ("Minivan", "Minivan"),
        ("SUV", "SUV"),
        ("Luxury", "Luxury"),
    ]

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("In Service", "In Service"),
        ("Maintenance", "Maintenance"),
        ("Out of Service", "Out of Service"),
    ]

    # Basic vehicle info
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)  # e.g., Toyota, Mercedes
    model = models.CharField(max_length=50)  # e.g., Camry, E-Class
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=30)
    vehicle_type = models.CharField(choices=VEHICLE_TYPE_CHOICES, max_length=20)

    # Capacity
    max_passengers = models.PositiveIntegerField()
    max_luggage = models.PositiveIntegerField()

    # Status
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="Available")
    is_active = models.BooleanField(default=True)

    # Documents
    registration_number = models.CharField(max_length=50, blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    insurance_expiry = models.DateField(null=True, blank=True)

    # Media
    image = models.ImageField(upload_to="vehicle_images", blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"
