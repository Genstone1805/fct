from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.conf import settings
from decimal import Decimal
import random


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)




class UserProfile(AbstractBaseUser, PermissionsMixin):
    # Required fields for AbstractBaseUser
    dp = models.ImageField(blank=True)
    full_name = models.CharField(max_length=80, blank=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    user_permissions = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    disabled = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class PasswordResetCode(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reset_codes')
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        """Check if the code is still valid (within 15 minutes and not used)"""
        if self.is_used:
            return False
        expiry_time = self.created_at + timezone.timedelta(minutes=15)
        return timezone.now() < expiry_time

    def __str__(self):
        return f"Reset code for {self.user.email}"