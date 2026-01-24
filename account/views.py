import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import UserProfile, PasswordResetCode
from .serializers import (
    SignUpSerializer,
    LoginSerializer,
    RequestPasswordResetSerializer,
    VerifyResetCodeSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
)


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

    ALL_PERMISSIONS = ['booking', 'drivers', 'routes', 'adminUsers']

    @extend_schema(request=SignUpSerializer, responses={201: UserProfileSerializer})
    def post(self, request):
        user = request.user
        serializer = SignUpSerializer(data=request.data)
        print(request.data)
        print("...........................................")
        if serializer.is_valid():
            print(serializer.validated_data)
            # Generate password
            generated_password = generate_password()

            # Get permissions from request
            permissions = serializer.validated_data.get('permissions', [])

            # Check if all permissions are selected (make user an admin)
            has_all_permissions = set(self.ALL_PERMISSIONS) == set(permissions)

            # Create user with the generated password
            user = UserProfile.objects.create_user(
                email=serializer.validated_data['email'],
                password=generated_password,
                phone_number=serializer.validated_data.get('phone_number'),
                full_name=serializer.validated_data.get('full_name', ''),
                added_by = user.full_name
            )

            # Set permissions
            if has_all_permissions or 'adminUsers' in permissions:
                user.is_staff = True
                user.user_permissions = self.ALL_PERMISSIONS
            else:
                user.user_permissions = permissions

            # Handle profile picture upload
            if 'dp' in serializer.validated_data:
                user.dp = serializer.validated_data['dp']

            user.save()

            # Send email with credentials
            subject = "Welcome to First Class Transfer - Your Login Credentials"
            permissions_text = ", ".join(permissions) if permissions else "None"
            role_text = "Administrator" if user.is_staff else "Staff"

            message = f"""
Hello {user.full_name or 'there'},

Welcome to First Class Transfer! Your account has been created successfully.

Here are your login credentials:

Email: {user.email}
Password: {generated_password}

Your Role: {role_text}
Your Permissions: {permissions_text}

Please keep these credentials safe and change your password after your first login.

Best regards,
First Class Transfer Team
            """
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_FROM,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't fail the registration
                print(f"Failed to send email: {e}")

            return Response(
                {
                    "message": "Account created successfully. Your login credentials have been sent to your email.",
                    "user": UserProfileSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_FROM,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send email: {e}")
                return Response(
                    {"error": "Failed to send verification email. Please try again."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_FROM,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Failed to send email: {e}")
                return Response(
                    {"error": "Password was reset but failed to send email. Please contact support."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
        return super().put(request, *args, **kwargs)

    @extend_schema(request=UserUpdateSerializer, responses={200: UserProfileSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(responses={204: None})
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
