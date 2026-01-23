from rest_framework.generics import ListAPIView

from .models import Route
from .serializers import RouteListSerializer


class RouteListView(ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteListSerializer
