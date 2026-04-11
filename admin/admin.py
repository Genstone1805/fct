from django.contrib import admin
from .models import Leads


@admin.register(Leads)
class LeadsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "created_at")
    search_fields = ("name", "email")
    ordering = ("-created_at",)
