import json
import os
from django.conf import settings
from datetime import timedelta
from django.db import transaction, IntegrityError
from django.db.models import Count, Sum, Q
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView, ListAPIView,
    RetrieveUpdateDestroyAPIView
)
from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from account.permissions import HasRoutePermission
from rest_framework.parsers import MultiPartParser, FormParser
from routes.models import Vehicle as RouteVehicle, RouteFAQ, Route
from vehicle.models import Vehicle
from booking.models import Booking
from account.models import UserProfile
from notifications.models import DriverNotification
from .serializers import ( CreateRouteSerializer )
from account.utils import log_user_activity, get_activity_log_path
from fct.parsers import recursive_underscoreize


class JSONFieldParserMixin:
    """Mixin to parse JSON string fields from multipart form data."""

    json_fields = [
        'what_makes_better', 'whats_included',
        'destination_highlights', 'ideal_for',
        'vehicle_options', 'faqs'
    ]

    def get_serializer(self, *args, **kwargs):
        """Parse JSON fields from multipart form data."""
        if 'data' in kwargs:
            data = kwargs['data']
            if hasattr(data, 'dict'):
                data = data.dict()
            else:
                data = dict(data)

            for field in self.json_fields:
                if field in data and isinstance(data[field], str):
                    try:
                        parsed = json.loads(data[field])
                        # Convert camelCase keys to snake_case in parsed JSON
                        data[field] = recursive_underscoreize(parsed)
                    except (json.JSONDecodeError, TypeError):
                        pass

            kwargs['data'] = data

        return super().get_serializer(*args, **kwargs)
    

class RouteListView(ListAPIView):
    """List all routes."""
    queryset = Route.objects.all()
    serializer_class = CreateRouteSerializer
    permission_classes = [HasRoutePermission]



class CreateRouteView(JSONFieldParserMixin, CreateAPIView):
    """Create a new route detail with optional nested vehicle options and FAQs."""
    queryset = Route.objects.all()
    serializer_class = CreateRouteSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [HasRoutePermission]

    def create(self, request, *args, **kwargs):
        user=request.user
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        vehicle_options_data = serializer.validated_data.pop('vehicle_options', [])
        faq_data = serializer.validated_data.pop('faqs', [])

        try:
            with transaction.atomic():
                route = Route.objects.create(**serializer.validated_data, added_by=user)

                for vehicle_data in vehicle_options_data:
                    RouteVehicle.objects.create(
                        route=route,
                        vehicle_type=vehicle_data.get('vehicle_type'),
                        max_passengers=vehicle_data.get('max_passengers'),
                        ideal_for=vehicle_data.get('ideal_for'),
                        fixed_price=vehicle_data.get('fixed_price')
                    )

                for faq_item in faq_data:
                    RouteFAQ.objects.create(
                        route=route,
                        question=faq_item.get('question'),
                        answer=faq_item.get('answer')
                    )

            log_user_activity(user, f"Created route: {route.from_location} → {route.to_location} ({route.route_id})", request)

            return Response({"message":"Route Created"}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response(
                {'error': 'Database integrity error', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            return Response(
                {'error': 'Validation error', 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to create route', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RetrieveUpdateDestroyRouteView(JSONFieldParserMixin, RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an existing route with nested vehicle options and FAQs."""
    queryset = Route.objects.all()
    serializer_class = CreateRouteSerializer
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = "route_id"
    permission_classes = [HasRoutePermission]

    def update(self, request, *args, **kwargs):
        user = request.user
        route = self.get_object()
        partial = kwargs.get('partial', False)
        serializer = self.get_serializer(instance=route, data=request.data, partial=partial)
        
        print(request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        vehicle_options_data = serializer.validated_data.pop('vehicle_options', [])
        faq_data = serializer.validated_data.pop('faqs', [])

        try:
            with transaction.atomic():
                route = serializer.save()

                if vehicle_options_data:
                    route.vehicle_options.all().delete()
                    for vehicle_data in vehicle_options_data:
                        RouteVehicle.objects.create(
                            route=route,
                            vehicle_type=vehicle_data.get('vehicle_type'),
                            max_passengers=vehicle_data.get('max_passengers'),
                            ideal_for=vehicle_data.get('ideal_for'),
                            fixed_price=vehicle_data.get('fixed_price')
                        )

                if faq_data:
                    route.faqs.all().delete()
                    for faq_item in faq_data:
                        RouteFAQ.objects.create(
                            route=route,
                            question=faq_item.get('question'),
                            answer=faq_item.get('answer')
                        )

            log_user_activity(user, f"Updated route: {route.from_location} → {route.to_location} ({route.route_id})", request)

            return Response({"message":"Route Updated"}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            return Response(
                {'error': 'Database integrity error', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            return Response(
                {'error': 'Validation error', 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to update route', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdminAnalyticsView(APIView):
    """
    Comprehensive analytics endpoint for super admin dashboard.
    Provides statistics across all aspects of the platform.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)
        start_of_year = today.replace(month=1, day=1)

        # ===== BOOKING STATISTICS =====
        total_bookings = Booking.objects.count()

        # Bookings by status
        bookings_by_status = dict(
            Booking.objects.values('status')
            .annotate(count=Count('id'))
            .values_list('status', 'count')
        )

        # Bookings by trip type
        bookings_by_trip_type = dict(
            Booking.objects.values('trip_type')
            .annotate(count=Count('id'))
            .values_list('trip_type', 'count')
        )

        # Bookings by payment status
        bookings_by_payment_status = dict(
            Booking.objects.values('payment_status')
            .annotate(count=Count('id'))
            .values_list('payment_status', 'count')
        )

        # Bookings by payment type
        bookings_by_payment_type = dict(
            Booking.objects.values('payment_type')
            .annotate(count=Count('id'))
            .values_list('payment_type', 'count')
        )

        # Bookings by time period
        bookings_by_time_period = dict(
            Booking.objects.values('time_period')
            .annotate(count=Count('id'))
            .values_list('time_period', 'count')
        )

        # Bookings by vehicle type
        bookings_by_vehicle_type = dict(
            Booking.objects.values('vehicle_type')
            .annotate(count=Count('id'))
            .values_list('vehicle_type', 'count')
        )

        # Time-based booking stats
        bookings_today = Booking.objects.filter(pickup_date=today).count()
        bookings_this_week = Booking.objects.filter(pickup_date__gte=start_of_week).count()
        bookings_this_month = Booking.objects.filter(pickup_date__gte=start_of_month).count()
        bookings_this_year = Booking.objects.filter(pickup_date__gte=start_of_year).count()

        # Upcoming bookings (future pickup dates, not cancelled/completed)
        upcoming_bookings = Booking.objects.filter(
            pickup_date__gte=today
        ).exclude(
            status__in=['Cancelled', 'Completed']
        ).count()

        # Bookings needing assignment (no driver or no vehicle)
        bookings_needing_driver = Booking.objects.filter(
            driver__isnull=True
        ).exclude(status__in=['Cancelled', 'Completed']).count()

        bookings_needing_vehicle = Booking.objects.filter(
            vehicle__isnull=True
        ).exclude(status__in=['Cancelled', 'Completed']).count()

        # ===== REVENUE STATISTICS =====
        total_revenue = Booking.objects.filter(
            status='Completed'
        ).aggregate(total=Sum('price'))['total'] or 0

        revenue_this_month = Booking.objects.filter(
            status='Completed',
            pickup_date__gte=start_of_month
        ).aggregate(total=Sum('price'))['total'] or 0

        revenue_this_year = Booking.objects.filter(
            status='Completed',
            pickup_date__gte=start_of_year
        ).aggregate(total=Sum('price'))['total'] or 0

        # Revenue by payment type
        revenue_by_payment_type = dict(
            Booking.objects.filter(status='Completed')
            .values('payment_type')
            .annotate(total=Sum('price'))
            .values_list('payment_type', 'total')
        )

        # ===== DRIVER STATISTICS =====
        total_drivers = UserProfile.objects.filter(is_driver=True).count()
        active_drivers = UserProfile.objects.filter(
            is_driver=True,
            is_active=True,
            disabled=False
        ).count()
        disabled_drivers = UserProfile.objects.filter(
            is_driver=True,
            disabled=True
        ).count()

        # Drivers with active bookings
        drivers_with_bookings = Booking.objects.filter(
            driver__isnull=False
        ).exclude(
            status__in=['Cancelled', 'Completed']
        ).values('driver').distinct().count()

        # Top drivers by completed bookings
        top_drivers = list(
            Booking.objects.filter(
                status='Completed',
                driver__isnull=False
            )
            .values('driver__id', 'driver__full_name', 'driver__email')
            .annotate(completed_bookings=Count('id'))
            .order_by('-completed_bookings')[:5]
        )

        # ===== VEHICLE STATISTICS =====
        total_vehicles = Vehicle.objects.count()

        vehicles_by_type = dict(
            Vehicle.objects.values('type')
            .annotate(count=Count('id'))
            .values_list('type', 'count')
        )

        # Vehicles with active bookings
        vehicles_with_bookings = Booking.objects.filter(
            vehicle__isnull=False
        ).exclude(
            status__in=['Cancelled', 'Completed']
        ).values('vehicle').distinct().count()

        # ===== ROUTE STATISTICS =====
        total_routes = Route.objects.count()

        # Most popular routes
        popular_routes = list(
            Booking.objects.values(
                'route__id',
                'route__from_location',
                'route__to_location'
            )
            .annotate(booking_count=Count('id'))
            .order_by('-booking_count')[:5]
        )

        # ===== USER STATISTICS =====
        total_users = UserProfile.objects.count()
        admin_users = UserProfile.objects.filter(is_superuser=True).count()
        staff_users = UserProfile.objects.filter(is_staff=True, is_superuser=False).count()
        regular_users = UserProfile.objects.filter(is_staff=False, is_driver=False).count()

        # ===== NOTIFICATION STATISTICS =====
        total_notifications = DriverNotification.objects.count()
        unread_notifications = DriverNotification.objects.filter(read=False).count()

        # ===== RECENT ACTIVITY =====
        recent_bookings = list(
            Booking.objects.select_related(
                'route', 'passenger_information', 'driver', 'vehicle'
            ).order_by('-id')[:10].values(
                'booking_id',
                'status',
                'pickup_date',
                'pickup_time',
                'route__from_location',
                'route__to_location',
                'passenger_information__full_name',
                'driver__full_name',
                'price'
            )
        )

        # ===== DAILY BOOKINGS TREND (Last 30 days) =====
        thirty_days_ago = today - timedelta(days=30)
        daily_bookings = list(
            Booking.objects.filter(pickup_date__gte=thirty_days_ago)
            .annotate(date=TruncDate('pickup_date'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        # ===== MONTHLY BOOKINGS TREND (Last 12 months) =====
        twelve_months_ago = today - timedelta(days=365)
        monthly_bookings = list(
            Booking.objects.filter(pickup_date__gte=twelve_months_ago)
            .annotate(month=TruncMonth('pickup_date'))
            .values('month')
            .annotate(count=Count('id'), revenue=Sum('price'))
            .order_by('month')
        )

        # Build response
        analytics = {
            'summary': {
                'total_bookings': total_bookings,
                'total_drivers': total_drivers,
                'total_vehicles': total_vehicles,
                'total_routes': total_routes,
                'total_revenue': total_revenue,
                'upcoming_bookings': upcoming_bookings,
            },
            'bookings': {
                'total': total_bookings,
                'by_status': {
                    'pending': bookings_by_status.get('Pending', 0),
                    'confirmed': bookings_by_status.get('Confirmed', 0),
                    'in_progress': bookings_by_status.get('In Progress', 0),
                    'completed': bookings_by_status.get('Completed', 0),
                    'cancelled': bookings_by_status.get('Cancelled', 0),
                },
                'by_trip_type': {
                    'one_way': bookings_by_trip_type.get('One Way', 0),
                    'return': bookings_by_trip_type.get('Return', 0),
                },
                'by_payment_status': {
                    'paid': bookings_by_payment_status.get('Paid', 0),
                    'paid_20_percent': bookings_by_payment_status.get('Paid 20%', 0),
                    'not_paid': bookings_by_payment_status.get('Not Paid', 0),
                },
                'by_payment_type': {
                    'cash': bookings_by_payment_type.get('Cash', 0),
                    'card': bookings_by_payment_type.get('Card', 0),
                },
                'by_time_period': {
                    'day_tariff': bookings_by_time_period.get('Day Tariff', 0),
                    'night_tariff': bookings_by_time_period.get('Night Tariff', 0),
                },
                'by_vehicle_type': bookings_by_vehicle_type,
                'time_based': {
                    'today': bookings_today,
                    'this_week': bookings_this_week,
                    'this_month': bookings_this_month,
                    'this_year': bookings_this_year,
                },
                'needing_attention': {
                    'needing_driver': bookings_needing_driver,
                    'needing_vehicle': bookings_needing_vehicle,
                },
            },
            'revenue': {
                'total': total_revenue,
                'this_month': revenue_this_month,
                'this_year': revenue_this_year,
                'by_payment_type': revenue_by_payment_type,
            },
            'drivers': {
                'total': total_drivers,
                'active': active_drivers,
                'disabled': disabled_drivers,
                'with_active_bookings': drivers_with_bookings,
                'top_performers': top_drivers,
            },
            'vehicles': {
                'total': total_vehicles,
                'by_type': vehicles_by_type,
                'with_active_bookings': vehicles_with_bookings,
            },
            'routes': {
                'total': total_routes,
                'most_popular': popular_routes,
            },
            'users': {
                'total': total_users,
                'admins': admin_users,
                'staff': staff_users,
                'regular': regular_users,
                'drivers': total_drivers,
            },
            'notifications': {
                'total': total_notifications,
                'unread': unread_notifications,
            },
            'trends': {
                'daily_bookings': daily_bookings,
                'monthly_bookings': monthly_bookings,
            },
            'recent_bookings': recent_bookings,
        }

        return Response(analytics)



class UserActivityLogView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        log_path = os.path.join(settings.BASE_DIR, "logs/user_activity.log")

        if not os.path.exists(log_path):
            return Response({"logs": []})

        with open(log_path, "r") as file:
            lines = file.readlines()

        # Optional: show latest entries only
        logs = lines[-200:]

        return Response({
            "logs": logs
        })
        
        
        


class DownloadActivityLogView(APIView):
    """Download the user activity log file. Admin only."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        log_path = get_activity_log_path()

        if not os.path.exists(log_path):
            raise Http404("Activity log file not found.")
        user = request.user
        log_user_activity(user, "Activity log: Download user activity log: ", request)
        return FileResponse(
            open(log_path, 'rb'),
            as_attachment=True,
            filename='user_activity.log'
        )