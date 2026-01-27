import os
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import FileResponse, Http404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAdminUser
from account.utils import log_user_activity
from rest_framework.validators import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from contextlib import suppress

from .models import UserProfile, PasswordResetCode
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    RequestPasswordResetSerializer,
    VerifyResetCodeSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
)
from .utils import get_activity_log_path


def get_tokens_for_user(user):
    """Generate JWT tokens for a user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def generate_password(length=10):
    """Generate a random password with letters, digits, and special characters."""
    characters = string.ascii_letters + string.digits + "!@#$%"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_code():
    """Generate a 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))


class SignUpView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    ALL_PERMISSIONS = ['booking', 'drivers', 'routes', 'vehicles', 'adminUsers']

    @extend_schema(request=SignUpSerializer, responses={201: UserProfileSerializer})
    def post(self, request):
        admin = request.user
        serializer = SignUpSerializer(data=request.data)
        user = None
        try:
            if not serializer.is_valid(raise_exception=True):
                return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
                
                
            generated_password = generate_password()
            
            permissions = serializer.validated_data.get('permissions', [])

            # Check if all permissions are selected (make user an admin)
            has_all_permissions = set(self.ALL_PERMISSIONS) == set(permissions)

            # Create user with the generated password
            user = UserProfile.objects.create_user(
                email=serializer.validated_data['email'],
                password=generated_password,
                phone_number=serializer.validated_data.get('phone_number'),
                full_name=serializer.validated_data.get('full_name', ''),
                added_by = admin.full_name
            )

            # Set permissions
            if has_all_permissions or 'adminUsers' in permissions:
                user.is_staff = True
                user.is_superuser = True
                user.user_permissions = self.ALL_PERMISSIONS
            else:
                user.user_permissions = permissions
                user.is_staff = True

            # Handle profile picture upload
            if 'dp' in serializer.validated_data:
                user.dp = serializer.validated_data['dp']

            user.save()
            log_user_activity(admin, f"Created User: {admin.full_name} → {admin.email} ({admin.id})", request)

            # Send email with credentials
            subject = "Welcome to First Class Transfer - Your Login Credentials"  
            permissions_text = ", ".join(permissions) if permissions else "None"
            role_text = "Administrator" if user.is_superuser else "Staff"
        
            message = f"""
                Hello {user.full_name or 'there'},

                Welcome to First Class Transfer! Your account has been created successfully.

                Here are your login credentials:

                Email: {user.email}
                Password: {generated_password}

                Your Role: {role_text}
                Your Permissions: {permissions_text}
                
                Next steps:
                - visit the login page on our site
                - Change your password immediately for security
                - Log into your dashboard

                Please keep these credentials safe and change your password after your first login.

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
            return Response(
                {'error': 'Validation error', 'details': e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to update route', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(request=LoginSerializer, responses={200: UserProfileSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.disabled:
                    return Response(
                        {"error": "This account has been disabled."},
                        status=status.HTTP_403_FORBIDDEN
                    )

                # Generate JWT tokens
                tokens = get_tokens_for_user(user)

                return Response(
                    {
                        "message": "Login successful",
                        "permissions": user.user_permissions,
                        "is_superuser": user.is_superuser,
                        "is_driver": user.is_driver,
                        "tokens": tokens
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(request=RequestPasswordResetSerializer)
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = UserProfile.objects.get(email=email)

            # Generate verification code
            code = generate_code()

            # Invalidate any existing codes for this user
            PasswordResetCode.objects.filter(user=user, is_used=False).update(is_used=True)

            # Create new reset code
            PasswordResetCode.objects.create(user=user, code=code)

            # Send email with verification code
            subject = "Password Reset Verification Code"
            message = f"""
Hello {user.full_name or 'there'},

You have requested to reset your password for your First Class Transfer account.

Your verification code is: {code}

This code will expire in 15 minutes.

If you did not request this, please ignore this email.

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
                {"message": "Verification code has been sent to your email."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyResetCodeView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(request=VerifyResetCodeSerializer)
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                user = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                return Response(
                    {"error": "No user found with this email."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Find the reset code
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=code,
                is_used=False
            ).first()

            if not reset_code:
                return Response(
                    {"error": "Invalid verification code."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not reset_code.is_valid():
                return Response(
                    {"error": "Verification code has expired. Please request a new one."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Mark code as used
            reset_code.is_used = True
            reset_code.save()

            # Generate new password
            new_password = generate_password()

            # Update user's password
            user.set_password(new_password)
            user.save()

            # Send email with new password
            subject = "Your New Password - First Class Transfer"
            message = f"""
Hello {user.full_name or 'there'},

Your password has been reset successfully.

Your new password is: {new_password}

Please log in with this new password and consider changing it for security.

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
                {"message": "Your new password has been sent to your email."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """List all users. Admin only."""
    queryset = UserProfile.objects.all().order_by('-date_joined')
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(responses={200: UserProfileSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a user. Admin only."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):  # type: ignore[override]
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserProfileSerializer

    @extend_schema(responses={200: UserProfileSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(request=UserUpdateSerializer, responses={200: UserProfileSerializer})
    def put(self, request, *args, **kwargs):
        admin = request.user
        user = self.get_object()
        log_user_activity(user, f"User Updated: {user.email} → {user.full_name} ({user.id}) by {admin.full_name}", request)
        return super().put(request, *args, **kwargs)

    @extend_schema(request=UserUpdateSerializer, responses={200: UserProfileSerializer})
    def patch(self, request, *args, **kwargs):
        admin = request.user
        user = self.get_object()
        log_user_activity(user, f"User Updated: {user.email} → {user.full_name} ({user.id}) by {admin.full_name}", request)
        return super().patch(request, *args, **kwargs)

    @extend_schema(responses={204: None})
    def delete(self, request, *args, **kwargs):
        admin = request.user
        user = self.get_object()
        log_user_activity(user, f"User Deleted: {user.email} → {user.full_name} ({user.id}) by {admin.full_name}", request)
        return super().delete(request, *args, **kwargs)


class DownloadActivityLogView(APIView):
    """Download the user activity log file. Admin only."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        log_path = get_activity_log_path()

        if not os.path.exists(log_path):
            raise Http404("Activity log file not found.")
        user = request.user
        log_user_activity(user, f"Activity log downloaded: {user.email} → {user.full_name} ({user.id})", request)
        return FileResponse(
            open(log_path, 'rb'),
            as_attachment=True,
            filename='user_activity.log'
        )


class UserUpdateUpView(RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]
    serializer_class = UserUpdateSerializer
    queryset = UserProfile.objects.all()
    lookup_field = "pk"

    ALL_PERMISSIONS = ['booking', 'drivers', 'routes', 'vehicles', 'adminUsers']

    def update(self, request, *args, **kwargs):
        admin = request.user
        user = self.get_object()

        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        try:
            if not serializer.is_valid(raise_exception=True):
                print(serializer.errors)
                return Response(
                {'error': 'Validation failed', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
            serializer.is_valid(raise_exception=True)

            permissions = serializer.validated_data.get('user_permissions', [])
            

            serializer.save()

            if set(permissions) == set(self.ALL_PERMISSIONS) or 'adminUsers' in permissions:
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = True
                user.is_superuser = False

            user.custom_permissions = permissions

            if 'dp' in serializer.validated_data:
                user.dp = serializer.validated_data['dp']

            user.save()

            log_user_activity(
                admin,
                f"Updated User: {user.full_name} ({user.email})",
                request
            )

            return Response(
                {"message": "User updated successfully"},
                status=status.HTTP_200_OK
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
