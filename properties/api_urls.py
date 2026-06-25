"""API URL router for properties app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    AgentViewSet, AgentSubscriptionViewSet, PropertyViewSet,
    TenantViewSet, LeaseViewSet, RentPaymentViewSet,
    MaintenanceRequestViewSet, InspectionViewSet,
    BuyerLeadViewSet, SellerLeadViewSet, BlogPostViewSet,
    ContactMessageViewSet, PaymentViewSet
)

router = DefaultRouter()
router.register(r'agents', AgentViewSet)
router.register(r'subscriptions', AgentSubscriptionViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'leases', LeaseViewSet)
router.register(r'rent-payments', RentPaymentViewSet)
router.register(r'maintenance-requests', MaintenanceRequestViewSet)
router.register(r'inspections', InspectionViewSet)
router.register(r'buyer-leads', BuyerLeadViewSet)
router.register(r'seller-leads', SellerLeadViewSet)
router.register(r'blog-posts', BlogPostViewSet)
router.register(r'contact-messages', ContactMessageViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
