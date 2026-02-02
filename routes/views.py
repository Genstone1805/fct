from rest_framework.generics import ListAPIView

from account.permissions import HasRoutesAPIKey
from .models import Route
from .serializers import RouteListSerializer


class RouteListView(ListAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteListSerializer
    permission_classes = [HasRoutesAPIKey]
