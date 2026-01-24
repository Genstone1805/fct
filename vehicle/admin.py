from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ["license_plate", "make", "model", "vehicle_type", "status", "is_active"]
    list_filter = ["vehicle_type", "status", "is_active"]
    search_fields = ["license_plate", "make", "model"]
