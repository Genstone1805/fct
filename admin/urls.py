from django.urls import path
from .views import (
    CreateVehicleView,
    CreateRouteFAQView,
    CreateRouteView,
    RouteListView,
)

urlpatterns = [
    path('routes/', RouteListView.as_view(), name='admin-route-list'),
    path('routes/create/', CreateRouteView.as_view(), name='admin-route-create'),
    path('vehicle-options/create/', CreateVehicleView.as_view(), name='admin-vehicle-create'),
    path('faq/create/', CreateRouteFAQView.as_view(), name='admin-faq-create'),
]
