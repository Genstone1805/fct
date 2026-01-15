from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from routes.models import VehicleOption, RouteFAQ, RouteDetail
from .serializers import CreateVehicleSerializer, CreateRouteFAQSerializer, CreateRouteSerializer


class CreateVehicleOptionView(CreateAPIView):
    """Create a new vehicle option for a route."""
    queryset = VehicleOption.objects.all()
    serializer_class = CreateVehicleSerializer


class CreateRouteFAQView(CreateAPIView):
    """Create a new FAQ for a route."""
    queryset = RouteFAQ.objects.all()
    serializer_class = CreateRouteFAQSerializer


class CreateRouteDetailView(CreateAPIView):
    """Create a new route detail."""
    queryset = RouteDetail.objects.all()
    serializer_class = CreateRouteSerializer
    parser_classes = [MultiPartParser, FormParser]


class RouteListView(ListAPIView):
    """List all routes for dropdown selection."""
    queryset = RouteDetail.objects.all()
    serializer_class = CreateRouteSerializer
