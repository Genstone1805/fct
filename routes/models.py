import secrets
import string
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


User = get_user_model()


class Vehicle(models.Model):
    VEHICLE_TYPE = [
        ("sedan", "sedan"),
        ("vclass","vclass")
    ]
    
    route = models.ForeignKey(
        'Route',
        on_delete=models.CASCADE,
        related_name='vehicle_options'
    )
    vehicle_type = models.CharField(choices=VEHICLE_TYPE, max_length=100)
    max_passengers = models.IntegerField()
    ideal_for = models.CharField(max_length=200)
    fixed_price = models.IntegerField()

    class Meta:
        verbose_name = 'Vehicle Option'
        verbose_name_plural = 'Vehicle Options'

    def __str__(self):
        return f"{self.vehicle_type} - {self.fixed_price}"


class RouteFAQ(models.Model):
    route = models.ForeignKey(
        'Route',
        on_delete=models.CASCADE,
        related_name='faqs'
    )
    question = models.CharField(max_length=500)
    answer = models.TextField()

    class Meta:
        verbose_name = 'Route FAQ'
        verbose_name_plural = 'Route FAQs'

    def __str__(self):
        return self.question


class Route(models.Model):
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    route_id = models.CharField(max_length=100, blank=True, null=True)

    slug = models.SlugField(max_length=200, unique=True, blank=True)
    from_location = models.CharField(max_length=200, verbose_name='From')
    to_location = models.CharField(max_length=200, verbose_name='To')

    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()

    hero_title = models.CharField(max_length=300)
    sub_headline = models.CharField(max_length=500)

    body = models.TextField()

    distance = models.CharField(max_length=50)
    time = models.CharField(max_length=50)  # Display string (e.g., "45 mins")
    duration_minutes = models.PositiveIntegerField(
        default=30,
        help_text="Duration of the route in minutes (used for availability calculation)"
    )
    sedan_price = models.IntegerField()
    van_price = models.IntegerField()

    what_makes_better = models.JSONField(default=list, blank=True)
    whats_included = models.JSONField(default=list)
    destination_highlights = models.JSONField(default=list, blank=True)
    ideal_for = models.JSONField(default=list, blank=True)

    # vehicle_options: accessed via reverse FK (VehicleOption.route)
    # faqs: accessed via reverse FK (RouteFAQ.route)

    image = models.ImageField(upload_to="Route Images")
    book_cta_label = models.CharField(max_length=300)
    book_cta_support = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Route Detail'
        verbose_name_plural = 'Route Details'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.from_location}-{self.to_location}")
            
        generate_booking_id = not self.route_id
        super().save(*args, **kwargs)

        if generate_booking_id:
            random_str = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(5))
            self.route_id = f"fct{random_str}{self.pk}"
            super().save(update_fields=['route_id'])

    def __str__(self):
        return f"{self.from_location} → {self.to_location}"
