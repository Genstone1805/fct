from django.urls import path
from .views import DriverListView, DriverDetailView, AvailableDriverListView

urlpatterns = [
    path('', DriverListView.as_view(), name='driver-list'),
    path('<int:pk>/', DriverDetailView.as_view(), name='driver-detail'),
    path('available/', AvailableDriverListView.as_view(), name='available-drivers'),
]
