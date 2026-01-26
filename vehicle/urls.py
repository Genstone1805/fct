from django.urls import path
from .views import (
    VehicleListCreateView, 
    VehicleDetailView, 
    AvailableVehicleListView
    )

urlpatterns = [
    path('', VehicleListCreateView.as_view(), name='vehicle-list'),
    path('available/', AvailableVehicleListView.as_view(), name='vehicle-available'),
    path('<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
]
