import secrets
import string

from django.db import models
from django.utils.text import slugify


class VehicleOption(models.Model):
    VEHICLE_TYPE = [
        ("Standard Car", "Standard Car"),
        ("Minivan","Minivan")
    ]
    route = models.ForeignKey(
        'RouteDetail',
        on_delete=models.CASCADE,
        related_name='vehicle_options'
    )
    vehicle_type = models.CharField(choices=VEHICLE_TYPE, max_length=100)
    max_passengers = models.IntegerField()
    ideal_for = models.CharField(max_length=200)
    fixed_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Vehicle Option'
        verbose_name_plural = 'Vehicle Options'

    def __str__(self):
        return f"{self.vehicle_type} - {self.fixed_price}"


class RouteFAQ(models.Model):
    route = models.ForeignKey(
        'RouteDetail',
        on_delete=models.CASCADE,
        related_name='faq'
    )
    question = models.CharField(max_length=500)
    answer = models.TextField()

    class Meta:
        verbose_name = 'Route FAQ'
        verbose_name_plural = 'Route FAQs'

    def __str__(self):
        return self.question


class RouteDetail(models.Model):
    booking_route_id = models.CharField(max_length=100, blank=True, null=True)

    slug = models.SlugField(max_length=200, unique=True, blank=True)
    from_location = models.CharField(max_length=200, verbose_name='From')
    to_location = models.CharField(max_length=200, verbose_name='To')

    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()

    hero_title = models.CharField(max_length=300)
    subheadline = models.CharField(max_length=500)

    body = models.TextField()

    distance = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    sedan_price = models.CharField(max_length=50)
    van_price = models.CharField(max_length=50)

    what_makes_better = models.JSONField(default=list, blank=True)
    whats_included = models.JSONField(default=list)
    destination_highlights = models.JSONField(default=list, blank=True)
    ideal_for = models.JSONField(default=list, blank=True)

    # vehicle_options: accessed via reverse FK (VehicleOption.route)
    # faq: accessed via reverse FK (RouteFAQ.route)

    image = models.ImageField(upload_to="Route Images")
    book_href = models.CharField(max_length=500)
    book_cta_label = models.CharField(max_length=100)
    book_cta_support = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Route Detail'
        verbose_name_plural = 'Route Details'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.from_location}-{self.to_location}")

        generate_booking_id = not self.booking_route_id
        super().save(*args, **kwargs)

        if generate_booking_id:
            random_str = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(5))
            self.booking_route_id = f"fct{random_str}{self.pk}"
            super().save(update_fields=['booking_route_id'])

    def __str__(self):
        return f"{self.from_location} → {self.to_location}"
