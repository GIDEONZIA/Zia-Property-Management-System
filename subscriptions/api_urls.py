"""API URL router for subscriptions app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import MpesaAuditLogViewSet, PremiumSubscriptionViewSet

router = DefaultRouter()
router.register(r'mpesa-audit-logs', MpesaAuditLogViewSet)
router.register(r'premium-subscriptions', PremiumSubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
