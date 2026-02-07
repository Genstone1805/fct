from django.db import models
from routes.models import Route
from vehicle.models import Vehicle
from django.contrib.auth import get_user_model

user = get_user_model()

import math
import secrets
import string

from django.db import models
from django.utils.text import slugify

class TransferInformation(models.Model):
  LUGGAGE_CHOICES = [
    ("Hand","Hand"),
    ("Medium","Medium"),
    ("Large","Large"),
    ("Extra Large","Extra Large"),
  ]

  flight_number = models.CharField(max_length=50)
  adults = models.IntegerField(default=1) 
  children = models.IntegerField(null=True, blank=True) 
  luggage = models.CharField(choices=LUGGAGE_CHOICES, max_length=80)

class PassengerDetail(models.Model):
  full_name = models.CharField(max_length=50)
  phone_number = models.CharField(max_length=50) 
  email_address = models.EmailField(max_length=30) 
  additional_information = models.TextField(null=True, blank=True)


class  Booking(models.Model):
  TRIP_TYPE_CHOICES = [
    ("One Way","One Way"),
    ("Return","Return")
  ]
  
  VEHICLE_TYPE = [
        ("sedan", "sedan"),
        ("vclass","vclass")
    ]

  TIME_PERIOD_CHOICES = [
    ("Day Tariff","Day Tariff"),
    ("Night Tariff","Night Tariff")
  ]

  PAYMENT_TYPES = [
    ("cash","cash"),
    ("card","card")
  ]
  
  PAYMENT_STATUS = [
    ("Paid","Paid"),
    ("Paid 20%","Paid 20%"),
  ]

  STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Assigned", "Assigned"),
    ("Completed", "Completed"),
    ("Cancelled", "Cancelled"),
  ]

  booking_id = models.CharField(max_length=100, blank=True, null=True)
  route = models.ForeignKey(Route, on_delete=models.CASCADE)
  booking_status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="Pending")
  amount_paid = models.FloatField(default=0.00)
  outstanding_amount = models.FloatField(default=0.00)
  total_amount = models.PositiveIntegerField(default=1)
  vehicle_type = models.CharField(choices=VEHICLE_TYPE, max_length=100)
  payment_type = models.CharField(choices=PAYMENT_TYPES, max_length=15 )
  payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=15)
  transaction_id = models.CharField(max_length=100, null=True, blank=True)
  trip_type = models.CharField(choices=TRIP_TYPE_CHOICES, max_length=15 )
  pickup_date = models.DateField()
  pickup_time = models.TimeField()
  time_period = models.CharField(choices=TIME_PERIOD_CHOICES, max_length=15 )
  return_date = models.DateField(null=True, blank=True)
  return_time = models.TimeField(null=True, blank=True)
  vehicle= models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
  driver = models.ForeignKey(user, on_delete=models.SET_NULL, null=True, blank=True)
  transfer_information = models.ForeignKey(TransferInformation, on_delete=models.CASCADE)
  passenger_information = models.ForeignKey(PassengerDetail, on_delete=models.CASCADE)

  class Meta:
        verbose_name = 'Booking Detail'
        verbose_name_plural = 'Booking Details'

  def save(self, *args, **kwargs):
      generate_booking_id = not self.booking_id
      
      self.amount_paid = math.ceil(float(self.amount_paid) * 100) / 100
      self.outstanding_amount = math.ceil(float(self.outstanding_amount) * 100) / 100

      if self.payment_type == "cash":
        self.payment_status = "Paid 20%"

      if self.payment_type == "card":
        self.payment_status = "Paid"

      super().save(*args, **kwargs)

      if generate_booking_id:
          random_str = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(5))
          self.booking_id = f"fct{random_str}{self.pk}"
          super().save(update_fields=['booking_id'])

  def __str__(self):
      return f"{self.booking_id}"
