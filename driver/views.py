from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from account.permissions import HasDriverPermission
from .models import Driver
from .serializers import DriverSerializer


class DriverViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Driver model.
    Requires 'drivers' permission or admin access.
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated, HasDriverPermission]
