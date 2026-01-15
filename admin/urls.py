from django.urls import path
from .views import (
    CreateVehicleOptionView,
    CreateRouteFAQView,
    CreateRouteDetailView,
    RouteListView,
)

urlpatterns = [
    path('routes/', RouteListView.as_view(), name='admin-route-list'),
    path('routes/create/', CreateRouteDetailView.as_view(), name='admin-route-create'),
    path('vehicle-options/create/', CreateVehicleOptionView.as_view(), name='admin-vehicle-create'),
    path('faq/create/', CreateRouteFAQView.as_view(), name='admin-faq-create'),
]
