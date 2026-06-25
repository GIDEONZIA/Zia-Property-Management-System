"""DRF ViewSets for payments app API."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import MpesaRentPayment, ReceiptLog
from properties.models import RentPayment
from .api_serializers import (
    MpesaRentPaymentSerializer, ReceiptLogSerializer, RentPaymentAPISerializer
)


class MpesaRentPaymentViewSet(viewsets.ModelViewSet):
    queryset = MpesaRentPayment.objects.all()
    serializer_class = MpesaRentPaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mpesa_receipt_number', 'tenant', 'lease', 'matched_by']


class ReceiptLogViewSet(viewsets.ModelViewSet):
    queryset = ReceiptLog.objects.all()
    serializer_class = ReceiptLogSerializer
    permission_classes = [IsAuthenticated]


class RentPaymentAPIViewSet(viewsets.ModelViewSet):
    queryset = RentPayment.objects.all()
    serializer_class = RentPaymentAPISerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tenant', 'lease', 'payment_method', 'receipt_number']
