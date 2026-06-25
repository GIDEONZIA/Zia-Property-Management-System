"""API URL router for payments app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import MpesaRentPaymentViewSet, ReceiptLogViewSet, RentPaymentAPIViewSet

router = DefaultRouter()
router.register(r'mpesa-payments', MpesaRentPaymentViewSet)
router.register(r'receipt-logs', ReceiptLogViewSet)
router.register(r'rent-payments', RentPaymentAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
