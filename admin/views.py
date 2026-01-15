import json
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from routes.models import VehicleOption, RouteFAQ, RouteDetail
from .serializers import CreateVehicleSerializer, CreateRouteFAQSerializer, CreateRouteSerializer


class CreateVehicleOptionView(CreateAPIView):
    """Create a new vehicle option for a route."""
    queryset = VehicleOption.objects.all()
    serializer_class = CreateVehicleSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class CreateRouteFAQView(CreateAPIView):
    """Create a new FAQ for a route."""
    queryset = RouteFAQ.objects.all()
    serializer_class = CreateRouteFAQSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class CreateRouteDetailView(CreateAPIView):
    """Create a new route detail with optional nested vehicle options and FAQs."""
    queryset = RouteDetail.objects.all()
    serializer_class = CreateRouteSerializer
    parser_classes = [MultiPartParser, FormParser]
    authentication_classes = []
    permission_classes = [AllowAny]

    # Store parsed nested data for use in perform_create
    _vehicle_options_data = []
    _faq_data = []

    def get_serializer(self, *args, **kwargs):
        """Parse JSON fields from multipart form data."""
        if args:
            data = args[0]
            if hasattr(data, 'dict'):
                data = data.dict()
            else:
                data = dict(data)

            # Parse JSON array fields
            json_fields = [
                'what_makes_better', 'whats_included',
                'destination_highlights', 'ideal_for',
                'vehicle_options', 'faq'
            ]
            
            for field in json_fields:
                if field in data and isinstance(data[field], str):
                    try:
                        data[field] = json.loads(data[field])
                    except (json.JSONDecodeError, TypeError):
                        pass

            # Extract and store nested data for later creation
            self._vehicle_options_data = data.pop('vehicle_options', []) or []
            self._faq_data = data.pop('faq', []) or []

            args = (data,) + args[1:]

        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        """Create the route and then create associated vehicle options and FAQs."""
        # Save the route
        route = serializer.save()

        # Create vehicle options and attach the route
        for vehicle_data in self._vehicle_options_data:
            VehicleOption.objects.create(
                route=route,
                vehicle_type=vehicle_data.get('vehicle_type'),
                max_passengers=vehicle_data.get('max_passengers'),
                ideal_for=vehicle_data.get('ideal_for'),
                fixed_price=vehicle_data.get('fixed_price')
            )

        # Create FAQs and attach the route
        for faq_data in self._faq_data:
            RouteFAQ.objects.create(
                route=route,
                question=faq_data.get('question'),
                answer=faq_data.get('answer')
            )


class RouteListView(ListAPIView):
    """List all routes for dropdown selection."""
    queryset = RouteDetail.objects.all()
    serializer_class = CreateRouteSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
