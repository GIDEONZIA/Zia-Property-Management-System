"""DRF Serializers for subscriptions app API."""
from rest_framework import serializers
from .models import MpesaAuditLog, PremiumSubscription


class MpesaAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaAuditLog
        fields = [
            'id', 'phone_number', 'transaction_type', 'amount',
            'reference', 'status', 'raw_response', 'created_at'
        ]


class PremiumSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumSubscription
        fields = [
            'id', 'agent', 'plan', 'is_active', 'start_date', 'end_date',
            'payment_method', 'transanction_id', 'verified', 'created_at'
        ]
