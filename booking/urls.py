from django.urls import path

from .views import (
    BookingCreateView,
    BookingListView,
    BookingDetailView,
    AssignDriverView,
    AssignVehicleView,
    AvailableDriversView,
    AvailableVehiclesView,
)

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('list/', BookingListView.as_view(), name='booking-list'),
    path('<str:booking_id>/detail/', BookingDetailView.as_view(), name='booking-detail'),
    path('<str:booking_id>/assign-driver/', AssignDriverView.as_view(), name='booking-assign-driver'),
    path('<str:booking_id>/assign-vehicle/', AssignVehicleView.as_view(), name='booking-assign-vehicle'),
    path('<str:booking_id>/available-drivers/', AvailableDriversView.as_view(), name='booking-available-drivers'),
    path('<str:booking_id>/available-vehicles/', AvailableVehiclesView.as_view(), name='booking-available-vehicles'),
]
