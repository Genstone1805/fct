from django.urls import path
from .views import DriverListView, RetrieveUpdateDestroyDriverView, AvailableDriverListView

urlpatterns = [
    path('', DriverListView.as_view(), name='driver-list'),
    path('<int:pk>/', RetrieveUpdateDestroyDriverView.as_view(), name='driver-detail'),
    path('available/', AvailableDriverListView.as_view(), name='available-drivers'),
]
