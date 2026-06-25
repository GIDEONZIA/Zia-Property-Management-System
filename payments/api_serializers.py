"""DRF Serializers for payments app API."""
from rest_framework import serializers
from .models import MpesaRentPayment, ReceiptLog
from properties.models import RentPayment


class MpesaRentPaymentSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(source='tenant.property_name', read_only=True)
    property_name = serializers.CharField(source='property.property_name', read_only=True)
    agent_name = serializers.CharField(source='agent.__str__', read_only=True)

    class Meta:
        model = MpesaRentPayment
        fields = [
            'id', 'tenant', 'lease', 'property', 'agent',
            'tenant_name', 'property_name', 'agent_name',
            'mpesa_receipt_number', 'phone_number', 'amount',
            'account_reference', 'transaction_type', 'transaction_time',
            'payer_name', 'matched_by', 'linked_rent_payment',
            'lease_rent_updated', 'tenant_sms_sent', 'agent_sms_sent',
            'tenant_email_sent', 'agent_email_sent',
            'created_at'
        ]


class ReceiptLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptLog
        fields = ['id', 'payment', 'recipient_type', 'channel', 'recipient', 'message', 'status', 'created_at']


class RentPaymentAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = RentPayment
        fields = ['id', 'tenant', 'lease', 'amount_paid', 'currency', 'payment_date', 'payment_method', 'receipt_number']
