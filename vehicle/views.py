from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from account.permissions import HasVehiclePermission, HasRoutesAPIKey
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
    permission_classes = [HasRoutesAPIKey, HasVehiclePermission]
    
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
            
            
            log_user_activity(user, f"Created Vehicle: {new_vehicle.make} {new_vehicle.model} ({new_vehicle.plate_number})", request)
            

            return Response(
                {
                    "message": "Vehicle created successfully",
                },
                status=status.HTTP_201_CREATED
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

class VehicleListCreateView(ListCreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [HasRoutesAPIKey, HasVehiclePermission]


class VehicleDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [HasRoutesAPIKey, HasVehiclePermission]
    
    
    def update(self, request, *args, **kwargs):
        user = request.user
        vehicle = self.get_object()
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance=vehicle, data=request.data, partial=partial)

        try:
            if not serializer.is_valid(raise_exception=True):
                return Response(
                    {'error': 'Validation failed', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                updated_vehicle = serializer.save()

            log_user_activity(
                user,
                f"Updated Vehicle: {updated_vehicle.make} {updated_vehicle.model} ({updated_vehicle.plate_number})",
                request
            )

            return Response(
                {
                    "message": "Vehicle updated successfully",
                },
                status=status.HTTP_200_OK
            )

        except ValidationError as e:
            return Response(
                {'error': 'Validation error', 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {'error': 'Failed to update vehicle', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        vehicle = self.get_object()
        vehicle_info = f"{vehicle.make} {vehicle.model} ({vehicle.plate_number})"

        response = super().destroy(request, *args, **kwargs)

        log_user_activity(
            request.user,
            f"Deleted Vehicle: {vehicle_info}",
            request
        )

        return response


class AvailableVehicleListView(ListAPIView):
    queryset = Vehicle.objects.filter()
    serializer_class = AvailableVehicleSerializer
    permission_classes = [HasRoutesAPIKey, HasVehiclePermission]
