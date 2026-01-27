from django.urls import path

from .views import (
    BookingCreateView,
    BookingListView,
    BookingUpdateView,
    AvailableDriversView,
    AvailableVehiclesView,
    AssignDriverVehicleView,
)

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('list/', BookingListView.as_view(), name='booking-list'),
    path('<str:booking_id>/update/', BookingUpdateView.as_view(), name='booking-update'),
    path('<str:booking_id>/assign/', AssignDriverVehicleView.as_view(), name='booking-assign'),
    path('available-drivers/', AvailableDriversView.as_view(), name='booking-available-drivers'),
    path('available-vehicles/', AvailableVehiclesView.as_view(), name='booking-available-vehicles'),
]
