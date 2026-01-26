from rest_framework import serializers
from routes.models import Vehicle, RouteFAQ, Route


class CreateVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'route', 'vehicle_type', 'max_passengers', 'ideal_for', 'fixed_price']


class UpdateVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'route', 'vehicle_type', 'max_passengers', 'ideal_for', 'fixed_price']


class CreateRouteFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteFAQ
        fields = ['id', 'route', 'question', 'answer']


class UpdateRouteFAQSerializer(serializers.ModelSerializer):
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


class VehicleInputSerializer(serializers.Serializer):
    """Serializer for validating vehicle option input data."""
    id = serializers.IntegerField(required=False)
    vehicle_type = serializers.ChoiceField(choices=Vehicle.VEHICLE_TYPE)
    max_passengers = serializers.IntegerField(min_value=1)
    ideal_for = serializers.CharField(max_length=200)
    fixed_price = serializers.IntegerField(min_value=0)


class FAQInputSerializer(serializers.Serializer):
    """Serializer for validating FAQ input data."""
    id = serializers.IntegerField(required=False)
    question = serializers.CharField(max_length=250)
    answer = serializers.CharField(max_length=700)


class CreateRouteSerializer(serializers.ModelSerializer):
    vehicle_options = VehicleInputSerializer(many=True, required=True)
    faqs = FAQInputSerializer(many=True, required=False)

    class Meta:
        model = Route
        fields = [
            'id',
            'route_id',
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
            'vehicle_options',
            'faqs',
        ]
        read_only_fields = ['route_id', 'slug']

    def to_representation(self, instance):
        """Include nested vehicle options and FAQs in the response."""
        rep = super().to_representation(instance)
        rep['vehicle_options'] = NestedVehicleSerializer(
            instance.vehicle_options.all(), many=True
        ).data
        rep['faqs'] = NestedFAQSerializer(
            instance.faqs.all(), many=True
        ).data
        return rep