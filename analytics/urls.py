from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_dashboard, name='analytics'),
    path('api/stats/', views.get_property_stats, name='api_stats'),
    path('api/types/', views.get_property_types, name='api_types'),
    path('api/trends/', views.get_monthly_trends, name='api_trends'),
    path('api/locations/', views.get_location_data, name='api_locations'),
    path('api/activity/', views.get_recent_activity, name='api_activity'),
]