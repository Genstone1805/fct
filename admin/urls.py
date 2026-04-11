from django.urls import path
from .views import (
    AdminAnalyticsView,
    CreateRouteView,
    DownloadActivityLogView,
    LeadCreateView,
    LeadDeleteView,
    LeadListView,
    LeadRetrieveView,
    RetrieveUpdateDestroyRouteView,
    RouteListView,
    UserActivityLogView
)

urlpatterns = [
    path('analytics/', AdminAnalyticsView.as_view(), name='admin-analytics'),
    path('leads/', LeadListView.as_view(), name='admin-lead-list'),
    path('leads/create/', LeadCreateView.as_view(), name='admin-lead-create'),
    path('leads/<int:pk>', LeadRetrieveView.as_view(), name='admin-lead-detail'),
    path('leads/<int:pk>/delete/', LeadDeleteView.as_view(), name='admin-lead-delete'),
    path('routes/', RouteListView.as_view(), name='admin-route-list'),
    path('routes/create/', CreateRouteView.as_view(), name='admin-route-create'),
    path('routes/<str:route_id>', RetrieveUpdateDestroyRouteView.as_view(), name='admin-route-update'),
    path('dashboard/', AdminAnalyticsView.as_view(), name='admin-dashboard'),
    path('activities/', UserActivityLogView.as_view(), name='user-log'),
    path('activities/download/', DownloadActivityLogView.as_view(), name='download-activity-log'),
]
