"""DRF ViewSets for subscriptions app API."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import MpesaAuditLog, PremiumSubscription
from .api_serializers import MpesaAuditLogSerializer, PremiumSubscriptionSerializer


class MpesaAuditLogViewSet(viewsets.ModelViewSet):
    queryset = MpesaAuditLog.objects.all()
    serializer_class = MpesaAuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['phone_number', 'transaction_type', 'status', 'reference']


class PremiumSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = PremiumSubscription.objects.all()
    serializer_class = PremiumSubscriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['agent', 'plan', 'is_active']
