import json
from django.db import transaction, IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView,
    RetrieveUpdateDestroyAPIView
)
from account.permissions import HasRoutePermission
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from routes.models import Vehicle, RouteFAQ, Route
from .serializers import ( CreateRouteSerializer )
from account.utils import log_user_activity


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
                        data[field] = json.loads(data[field])
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
                    Vehicle.objects.create(
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

            log_user_activity(user, f"Created route: {route.from_location} → {route.to_location} ({route.route_id})")

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
        
        print("===============DATA SENT========================")
        print(request.data)
        print("===============DATA SENT========================")

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
                        Vehicle.objects.create(
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

            log_user_activity(user, f"Updated route: {route.from_location} → {route.to_location} ({route.route_id})")

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


# class VehicleDetailView(RetrieveUpdateDestroyAPIView):
#     """Retrieve, update or delete a vehicle option."""
#     queryset = Vehicle.objects.all()
#     authentication_classes = []
#     serializer_class = UpdateVehicleSerializer
#     permission_classes = [AllowAny]
#     lookup_field="pk"


# class FAQDetailView(RetrieveUpdateDestroyAPIView):
#     """Retrieve, update or delete a FAQ."""
#     queryset = RouteFAQ.objects.all()
#     authentication_classes = []
#     serializer_class = UpdateRouteFAQSerializer
#     lookup_field="pk"
#     permission_classes = [AllowAny]
