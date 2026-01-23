from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignUpView,
    LoginView,
    RequestPasswordResetView,
    VerifyResetCodeView,
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('password-reset/request/', RequestPasswordResetView.as_view(), name='password-reset-request'),
    path('password-reset/verify/', VerifyResetCodeView.as_view(), name='password-reset-verify'),
]
