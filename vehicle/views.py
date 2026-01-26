from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from account.permissions import HasVehiclePermission
from .models import Vehicle
from .serializers import VehicleSerializer, AvailableVehicleSerializer
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from account.utils import log_user_activity
from rest_framework.validators import ValidationError

class VehicleCreateCreateView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [HasVehiclePermission]
    
    def create(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        try:
            if not serializer.is_valid(raise_exception=True):
                return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
                
            with transaction.atomic():
                new_vehicle = Vehicle.objects.create(**serializer.validated_data, added_by=user)
            
            
            log_user_activity(user, f"Vehicle Created: {new_vehicle.make} → {new_vehicle.model} ({new_vehicle.year}) by {user.full_name}", request)
            

            return Response(
                {
                    "message": "Vehicle created successfully",
                },
                status=status.HTTP_201_CREATED
            )
                
        except ValidationError as e:
            print(serializer.errors)
            return Response(
                {'error': 'Validation error', 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            print(serializer.errors)
            return Response(
                {'error': 'Failed to update route', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class VehicleListCreateView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [HasVehiclePermission]


class VehicleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [HasVehiclePermission]
    
    
    def update(self, request, *args, **kwargs):
        user = request.user
        vehicle = self.get_object()
        partial = kwargs.get('partial', False)
        serializer = self.get_serializer(instance=vehicle, data=request.data, partial=partial)
        

        if not serializer.is_valid():
            return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if not serializer.is_valid(raise_exception=True):
                return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
                
            with transaction.atomic():
                new_vehicle = Vehicle.objects.create(**serializer.validated_data, added_by=user)
            
            
            log_user_activity(user, f"Vehicle Updated: {new_vehicle.make} → {new_vehicle.model} ({new_vehicle.year}) by {user.full_name}", request)
            

            return Response(
                {
                    "message": "Vehicle created successfully",
                },
                status=status.HTTP_201_CREATED
            )
                
        except ValidationError as e:
            print(serializer.errors)
            return Response(
                {'error': 'Validation error', 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            print(serializer.errors)
            return Response(
                {'error': 'Failed to update route', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AvailableVehicleListView(ListAPIView):
    queryset = Vehicle.objects.filter()
    serializer_class = AvailableVehicleSerializer
    permission_classes = [HasVehiclePermission]
