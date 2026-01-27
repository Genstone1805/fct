from django.urls import path
from .views import (
    DriverListView, 
    RetrieveUpdateDestroyDriverView, 
    AvailableDriverListView,
    CreateDriverView,
    RetrieveDriverView
    )

urlpatterns = [
    path('', DriverListView.as_view(), name='driver-list'),
    path('<int:pk>/', RetrieveUpdateDestroyDriverView.as_view(), name='driver-detail'),
    path('available/', AvailableDriverListView.as_view(), name='available-drivers'),
    path('create/', CreateDriverView.as_view(), name='create-drivers'),
    path('dashboard/', RetrieveDriverView.as_view(), name='drivers-dashboard'),
]
