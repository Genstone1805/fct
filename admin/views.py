import json
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView,
    UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from routes.models import Vehicle, RouteFAQ, Route
from .serializers import (
    CreateVehicleSerializer, UpdateVehicleSerializer,
    CreateRouteFAQSerializer, UpdateRouteFAQSerializer,
    CreateRouteSerializer, UpdateRouteSerializer
)


class JSONFieldParserMixin:
    """Mixin to parse JSON string fields from multipart form data."""

    json_fields = [
        'what_makes_better', 'whats_included',
        'destination_highlights', 'ideal_for',
        'vehicle_options', 'faq'
    ]

    def get_serializer(self, *args, **kwargs):
        """Parse JSON fields from multipart form data."""
        if 'data' in kwargs:
            data = kwargs['data']
            if hasattr(data, 'dict'):
                data = data.dict()
            else:
                data = dict(data)

            for field in self.json_fields:
                if field in data and isinstance(data[field], str):
                    try:
                        data[field] = json.loads(data[field])
                    except (json.JSONDecodeError, TypeError):
                        pass

            kwargs['data'] = data

        return super().get_serializer(*args, **kwargs)


class CreateVehicleView(CreateAPIView):
    """Create a new vehicle option for a route."""
    queryset = Vehicle.objects.all()
    serializer_class = CreateVehicleSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class CreateRouteFAQView(CreateAPIView):
    """Create a new FAQ for a route."""
    queryset = RouteFAQ.objects.all()
    serializer_class = CreateRouteFAQSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class CreateRouteView(JSONFieldParserMixin, CreateAPIView):
    """Create a new route detail with optional nested vehicle options and FAQs."""
    queryset = Route.objects.all()
    serializer_class = CreateRouteSerializer
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = []
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Create the route and then create associated vehicle options and FAQs."""
        vehicle_options_data = serializer.validated_data.pop('vehicle_options', [])
        faq_data = serializer.validated_data.pop('faq', [])

        route = serializer.save()

        for vehicle_data in vehicle_options_data:
            Vehicle.objects.create(
                route=route,
                vehicle_type=vehicle_data.get('vehicle_type'),
                max_passengers=vehicle_data.get('max_passengers'),
                ideal_for=vehicle_data.get('ideal_for'),
                fixed_price=vehicle_data.get('fixed_price')
            )

        for faq_item in faq_data:
            RouteFAQ.objects.create(
                route=route,
                question=faq_item.get('question'),
                answer=faq_item.get('answer')
            )


class RouteListView(ListAPIView):
    """List all routes."""
    queryset = Route.objects.all()
    serializer_class = CreateRouteSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class RouteDetailView(RetrieveAPIView):
    """Retrieve a single route by ID."""
    queryset = Route.objects.all()
    serializer_class = CreateRouteSerializer
    authentication_classes = []
    lookup_field = "booking_route_id"
    permission_classes = [AllowAny]


class UpdateRouteView(JSONFieldParserMixin, RetrieveUpdateDestroyAPIView):
    """Update an existing route with optional nested vehicle options and FAQs."""
    queryset = Route.objects.all()
    serializer_class = UpdateRouteSerializer
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = []
    lookup_field = "booking_route_id"
    permission_classes = [AllowAny]


class VehicleDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a vehicle option."""
    queryset = Vehicle.objects.all()
    authentication_classes = []
    serializer_class = UpdateVehicleSerializer
    permission_classes = [AllowAny]
    lookup_field="pk"


class FAQDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a FAQ."""
    queryset = RouteFAQ.objects.all()
    authentication_classes = []
    serializer_class = UpdateRouteFAQSerializer
    lookup_field="pk"
    permission_classes = [AllowAny]
