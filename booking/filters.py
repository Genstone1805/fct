import django_filters

from .models import Booking


class BookingFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    pickup_date = django_filters.DateFilter(field_name='pickup_date', lookup_expr='exact')
    return_date = django_filters.DateFilter(field_name='return_date', lookup_expr='exact')
    payment_status = django_filters.CharFilter(field_name='payment_status', lookup_expr='exact')
    passenger_name = django_filters.CharFilter(
        field_name='passenger_information__full_name',
        lookup_expr='icontains'
    )
    vehicle_type = django_filters.CharFilter(
        field_name='vehicle__vehicle_type',
        lookup_expr='exact'
    )
    from_location = django_filters.CharFilter(
        field_name='route__from_location',
        lookup_expr='icontains'
    )
    to_location = django_filters.CharFilter(
        field_name='route__to_location',
        lookup_expr='icontains'
    )

    class Meta:
        model = Booking
        fields = [
            'status',
            'pickup_date',
            'return_date',
            'passenger_name',
            'vehicle_type',
            'from_location',
            'to_location',
            'payment_status',
        ]
