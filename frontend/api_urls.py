"""API URL router for frontend app."""
from django.urls import path
from .api_views import (
    RentReminderLogAPIView, TenantPortalUserAPIView, WelcomePackDeliveryAPIView
)

urlpatterns = [
    path('rent-reminders/', RentReminderLogAPIView.as_view(), name='api_rent_reminders'),
    path('tenant-portal-users/', TenantPortalUserAPIView.as_view(), name='api_tenant_portal_users'),
    path('welcome-pack-deliveries/', WelcomePackDeliveryAPIView.as_view(), name='api_welcome_pack_deliveries'),
]
