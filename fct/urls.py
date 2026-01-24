from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("account.urls")),
    path('routes/', include("routes.urls")),
    path('control/', include("admin.urls")),
    path('booking/', include("booking.urls")),
    path('drivers/', include("driver.urls")),
    path('account/', include("account.urls")),
    
    # Templates
    path('template/manage/', TemplateView.as_view(template_name='admin/dashboard.html'), name='admin-dashboard'),
    path('template/login/', TemplateView.as_view(template_name='admin/login.html'), name='login-page'),
    path('template/password-reset/', TemplateView.as_view(template_name='admin/password-reset.html'), name='password-reset-page'),
    
    # YOUR PATTERNS
    path('download-docs/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
