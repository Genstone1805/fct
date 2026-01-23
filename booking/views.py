from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .models import Booking
from .serializers import BookingCreateSerializer


class BookingCreateView(CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer
    permission_classes = [AllowAny]
