from django.db import models
from routes.models import Route, Vehicle

class TransferInformation(models.Model):
  LUGGAGE_CHOICES = [
    ("Hand luggage only","Hand luggage only"),
    ("Medium (1–2 suitcases)","Medium (1–2 suitcases)"),
    ("Large (3–4 suitcases)","Large (3–4 suitcases)"),
    ("Extra large (5+ suitcases)","Extra large (5+ suitcases)")
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


class Booking(models.Model):
  TRIP_TYPE_CHOICES = [
    ("One Way","One Way"),
    ("Return","Return")
  ]

  TIME_PERIOD_CHOICES = [
    ("Day Tariff","Day Tariff"),
    ("Night Tariff","Night Tariff")
  ]

  PAYMENT_CHOICES = [
    ("Cash","Cash"),
    ("Card","Card")
  ]
  
  PAYMENT_CHOICES = [
    ("Pending","Pending"),
    ("Processing","Processing"),
    ("Completed","Completed")
  ]


  status = models.CharField(choices=PAYMENT_CHOICES, max_length=15 )
  payment_type = models.CharField(choices=PAYMENT_CHOICES, max_length=15 )
  trip_type = models.CharField(choices=TRIP_TYPE_CHOICES, max_length=15 )
  route = models.ForeignKey(Route, on_delete=models.CASCADE)
  payment_id = models.CharField(max_length=25, null=True, blank=True)
  vehicle_type= models.ForeignKey(Vehicle, on_delete=models.CASCADE)
  pickup_date = models.DateField()
  pickup_time = models.TimeField()
  time_period = models.CharField(choices=TIME_PERIOD_CHOICES, max_length=15 )
  return_date = models.DateField(null=True, blank=True)
  return_time = models.TimeField(null=True, blank=True)

  transfer_information = models.ForeignKey(TransferInformation, on_delete=models.CASCADE)
  passenger_information = models.ForeignKey(PassengerDetail, on_delete=models.CASCADE)
