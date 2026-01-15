from rest_framework.generics import ListAPIView

from .models import RouteDetail
from .serializers import RouteDetailSerializer


class RouteListView(ListAPIView):
    queryset = RouteDetail.objects.all()
    serializer_class = RouteDetailSerializer
