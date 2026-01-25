from django.urls import path
from .views import (
    CreateVehicleView,
    CreateRouteFAQView,
    CreateRouteView,
    RouteListView,
    RetrieveUpdateDestroyRouteView,
    VehicleDetailView,
    FAQDetailView,
)

urlpatterns = [
    path('routes/', RouteListView.as_view(), name='admin-route-list'),
    path('routes/create/', CreateRouteView.as_view(), name='admin-route-create'),
    path('routes/<str:route_id>/detail/', RetrieveUpdateDestroyRouteView.as_view(), name='admin-route-update'),
    path('vehicle-options/create/', CreateVehicleView.as_view(), name='admin-vehicle-create'),
    path('vehicle-options/<int:pk>/detail/', VehicleDetailView.as_view(), name='admin-vehicle-detail'),
    path('faq/create/', CreateRouteFAQView.as_view(), name='admin-faq-create'),
    path('faq/<int:pk>/detail/', FAQDetailView.as_view(), name='admin-faq-detail'),
]
