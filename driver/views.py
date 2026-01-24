from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from account.permissions import HasDriverPermission
from .models import Driver
from .serializers import DriverSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated, HasDriverPermission]
