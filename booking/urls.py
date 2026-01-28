from django.urls import path

from .views import (
    BookingCreateView,
    BookingListView,
    BookingUpdateView,
    AvailableDriversView,
    AvailableVehiclesView,
    AssignDriverVehicleView,
    BookingStatusUpdateView,
    RescheduleBookingView,
    UserBookingsView
)

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('list/', BookingListView.as_view(), name='booking-list'),
    path('<str:booking_id>/update/', BookingUpdateView.as_view(), name='booking-update'),
    path('<str:booking_id>/assign/', AssignDriverVehicleView.as_view(), name='booking-assign'),
    path('<str:booking_id>/update-status/', BookingStatusUpdateView.as_view(), name='update-booking-status'),
    path('<str:booking_id>/reschedule/', RescheduleBookingView.as_view(), name='booking-reschedule'),
    path('<str:booking_id>/available-drivers/', AvailableDriversView.as_view(), name='booking-available-drivers'),
    path('<str:booking_id>/available-vehicles/', AvailableVehiclesView.as_view(), name='booking-available-vehicles'),
    path('assigned-bookings/<int:pk>', UserBookingsView.as_view(), name='assigned-bookings'),
]
