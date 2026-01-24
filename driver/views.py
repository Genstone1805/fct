from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from account.permissions import HasDriverPermission
from .models import Driver
from .serializers import DriverSerializer, AvailableDriverSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated, HasDriverPermission]


class AvailableDriverListView(ListAPIView):
    queryset = Driver.objects.filter(status="Available")
    serializer_class = AvailableDriverSerializer
    permission_classes = [IsAuthenticated]
