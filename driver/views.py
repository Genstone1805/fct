from rest_framework import generics
from rest_framework.response import Response
from django_filters import rest_framework as filters
from account.models import UserProfile
from .serializers import DriverSerializer, AvailableDriverSerializer, DriverListSerializer
from account.permissions import HasDriverPermission
from fct.utils import CustomPagination
from account.utils import log_user_activity
from django.db import transaction, IntegrityError

class DriverFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = UserProfile
        fields = ['status', 'name', 'email']


class DriverListView(generics.ListAPIView):
    """List all users where is_driver=True"""
    serializer_class = DriverListSerializer
    permission_classes = [HasDriverPermission]
    queryset = UserProfile.objects.filter(is_driver=True)
    pagination_class = CustomPagination
    filterset_class = DriverFilter


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_drivers = UserProfile.objects.filter(is_driver=True).count()
        available_drivers = UserProfile.objects.filter(is_driver=True, status="Available").count()
    
        off_duty_drivers = UserProfile.objects.filter(is_driver=True, status="Unavailable").count()
        

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['all'] = total_drivers
            response.data['available'] = available_drivers
            response.data['unavailable'] = off_duty_drivers
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'results': serializer.data,
            'all': total_drivers,
            'available': available_drivers,         
            'unavailable': available_drivers,         
        })
    
    

class RetrieveUpdateDestroyDriverView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, Update, or Destroy a driver"""
    serializer_class = DriverSerializer
    queryset = UserProfile.objects.filter(is_driver=True)
    lookup_field = 'pk'
    permission_classes = [HasDriverPermission]
    
    def update(self, request, *args, **kwargs):
        user = request.user
        driver = self.get_object()
        partial = kwargs.get["partial", False]
        serializer = self.get_serializer(instance=driver, data=request.data, partial=partial)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                driver = serializer.save()

            log_user_activity(user, f"Updated Driver: {driver.email} → {driver.full_name} ({driver.id})", request)

            return Response({"message":"Driver Updated"}, status=status.HTTP_200_OK)
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


class AvailableDriverListView(generics.ListAPIView):
    """List all available drivers (is_driver=True and status='Available')"""
    serializer_class = AvailableDriverSerializer
    permission_classes = [HasDriverPermission]
    queryset = UserProfile.objects.filter(is_driver=True, status='Available')
