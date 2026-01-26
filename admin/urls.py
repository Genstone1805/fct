from django.urls import path
from .views import (
    CreateRouteView,
    RouteListView,
    RetrieveUpdateDestroyRouteView,
)

urlpatterns = [
    path('routes/', RouteListView.as_view(), name='admin-route-list'),
    path('routes/create/', CreateRouteView.as_view(), name='admin-route-create'),
    path('routes/<str:route_id>', RetrieveUpdateDestroyRouteView.as_view(), name='admin-route-update'),
]
