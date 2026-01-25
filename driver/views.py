from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from account.models import UserProfile
from .serializers import DriverSerializer, AvailableDriverSerializer


class DriverListView(generics.ListAPIView):
    """List all users where is_driver=True"""
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(is_driver=True)


class DriverDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update, or Destroy a driver"""
    serializer_class = DriverSerializer
    queryset = UserProfile.objects.filter(is_driver=True)
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]


class AvailableDriverListView(generics.ListAPIView):
    """List all available drivers (is_driver=True and status='Available')"""
    serializer_class = AvailableDriverSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(is_driver=True, status='Available')
