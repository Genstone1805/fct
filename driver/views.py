from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema
from account.serializers import SignUpSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework import status
from account.views import generate_password
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.validators import ValidationError
from contextlib import suppress



from rest_framework import generics
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
        
        


class CreateDriverView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    @extend_schema(request=SignUpSerializer, responses={201: UserProfileSerializer})
    def post(self, request):
        admin = request.user
        serializer = SignUpSerializer(data=request.data)
        user = None
        try:
            if not serializer.is_valid(raise_exception=True):
                print(serializer.errors)
                return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
                
            print(request.data)
                
                
            generated_password = generate_password()
            
            user = UserProfile.objects.create_user(
                email=serializer.validated_data['email'],
                password=generated_password,
                phone_number=serializer.validated_data.get('phone_number'),
                full_name=serializer.validated_data.get('full_name', ''),
                license_number = serializer.validated_data.get('license_number', ''),
                added_by = admin.full_name,
                is_driver = True
            )
            
            # Handle profile picture upload
            if 'dp' in serializer.validated_data:
                user.dp = serializer.validated_data['dp']
            
            user.save()
            
            log_user_activity(admin, f"Created Driver: {admin.full_name} → {admin.email} ({admin.id})", request)

            # Send email with credentials
            subject = "Welcome to First Class Transfer - Your Login Credentials"
            
            message = f"""
                Hello {user.full_name or 'there'},

                Welcome to First Class Transfer!  
                You’ve been successfully onboarded as a **Driver** on our platform.

                Below are your login details:

                Email: {user.email}  
                Temporary Password: {generated_password}

                Role: Driver  

                Next steps:
                - visit the login page on our site
                - Change your password immediately for security
                - Log into your dashboard

                You’re now part of our trusted driver network, and we’re excited to have you on board. If you need support, our team is ready to assist.

                Drive safe and deliver excellence.

                Best regards,  
                First Class Transfer Team
            """
            with suppress(Exception):
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_FROM,
                    [user.email],
                    fail_silently=False,
                )

            return Response(
                {
                    "message": "Account created successfully. Your login credentials have been sent to your email.",
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

class DriverListView(generics.ListAPIView):
    """List all users where is_driver=True"""
    serializer_class = DriverListSerializer
    # permission_classes = [HasDriverPermission]
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
