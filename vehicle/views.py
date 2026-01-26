from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from account.permissions import HasVehiclePermission
from .models import Vehicle
from .serializers import VehicleSerializer, AvailableVehicleSerializer


class VehicleListCreateView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [HasVehiclePermission]


class VehicleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [HasVehiclePermission]


class AvailableVehicleListView(ListAPIView):
    queryset = Vehicle.objects.filter(status="Available")
    serializer_class = AvailableVehicleSerializer
    permission_classes = [HasVehiclePermission]
