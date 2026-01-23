from rest_framework import serializers
from routes.models import Vehicle, RouteFAQ, Route


class CreateVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'route', 'vehicle_type', 'max_passengers', 'ideal_for', 'fixed_price']


class CreateRouteFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteFAQ
        fields = ['id', 'route', 'question', 'answer']


class NestedVehicleSerializer(serializers.ModelSerializer):
    """Serializer for vehicle options when nested in route response."""
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_type', 'max_passengers', 'ideal_for', 'fixed_price']


class NestedFAQSerializer(serializers.ModelSerializer):
    """Serializer for FAQs when nested in route response."""
    class Meta:
        model = RouteFAQ
        fields = ['id', 'question', 'answer']


class CreateRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = [
            'id',
            'booking_route_id',
            'slug',
            'from_location',
            'to_location',
            'meta_title',
            'meta_description',
            'hero_title',
            'sub_headline',
            'body',
            'distance',
            'time',
            'sedan_price',
            'van_price',
            'what_makes_better',
            'whats_included',
            'destination_highlights',
            'ideal_for',
            'image',
            'book_cta_label',
            'book_cta_support',
        ]
        read_only_fields = ['booking_route_id', 'slug']

    def to_representation(self, instance):
        """Include nested vehicle options and FAQs in the response."""
        rep = super().to_representation(instance)
        rep['vehicle_options'] = NestedVehicleSerializer(
            instance.vehicle_options.all(), many=True
        ).data
        rep['faq'] = NestedFAQSerializer(
            instance.faq.all(), many=True
        ).data
        return rep
