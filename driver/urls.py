from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DriverViewSet, AvailableDriverListView

router = DefaultRouter()
router.register(r'', DriverViewSet, basename='driver')

urlpatterns = [
    path('available/', AvailableDriverListView.as_view(), name='driver-available'),
    path('', include(router.urls)),
]
