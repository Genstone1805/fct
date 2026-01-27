from django.urls import path
from .views import (
    CreateRouteView,
    RouteListView,
    RetrieveUpdateDestroyRouteView,
    AdminAnalyticsView,
    AdminAnalyticsView
)

urlpatterns = [
    path('analytics/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('routes/', RouteListView.as_view(), name='admin-route-list'),
    path('routes/create/', CreateRouteView.as_view(), name='admin-route-create'),
    path('routes/<str:route_id>', RetrieveUpdateDestroyRouteView.as_view(), name='admin-route-update'),
    path('dashboard/', AdminAnalyticsView.as_view(), name='admin-dashboard'),
]
