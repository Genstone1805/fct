from rest_framework import serializers

from .models import Vehicle, RouteFAQ, Route

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['vehicle_type', 'max_passengers', 'ideal_for', 'fixed_price']

class RouteFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteFAQ
        fields = ['question', 'answer']

class RouteListSerializer(serializers.ModelSerializer):
    vehicle_options = serializers.SerializerMethodField()
    faq = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = [
            'booking_route_id',
            'slug',
            'from_location',
            'to_location',
            'meta_title',
            'meta_description',
            'hero_title',
            'subheadline',
            'body',
            'distance',
            'time',
            'sedan_price',
            'van_price',
            'what_makes_better',
            'whats_included',
            'destination_highlights',
            'ideal_for',
            'vehicle_options',
            'faq',
            'image',
            'book_href',
            'book_cta_label',
            'book_cta_support',
        ]
        read_only_fields = ['booking_route_id', 'slug']

    def get_vehicle_options(self, obj):
        options = Vehicle.objects.filter(route=obj)
        return VehicleSerializer(options, many=True).data

    def get_faq(self, obj):
        faqs = RouteFAQ.objects.filter(route=obj)
        return RouteFAQSerializer(faqs, many=True).data