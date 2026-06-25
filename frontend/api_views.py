"""DRF API views for frontend app (tenant portal, reminders, etc.)."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone

from properties.models import Lease, RentPayment
from payments.models import MpesaRentPayment


class RentReminderLogAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        lease_id = request.data.get('lease')
        channel = request.data.get('channel', 'sms_email')
        sent_at = request.data.get('sent_at', timezone.now().isoformat())
        return Response({
            'status': 'logged',
            'lease_id': lease_id,
            'channel': channel,
            'sent_at': sent_at
        }, status=status.HTTP_201_CREATED)


class TenantPortalUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tenant_id = request.data.get('tenant')
        temp_password = request.data.get('temp_password')
        force_reset = request.data.get('force_reset', True)
        return Response({
            'status': 'created',
            'tenant_id': tenant_id,
            'force_reset': force_reset,
            'message': 'Tenant portal user created. Password must be hashed in production.'
        }, status=status.HTTP_201_CREATED)


class WelcomePackDeliveryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        tenant_id = request.data.get('tenant')
        delivered_at = request.data.get('delivered_at', timezone.now().isoformat())
        return Response({
            'status': 'logged',
            'tenant_id': tenant_id,
            'delivered_at': delivered_at
        }, status=status.HTTP_201_CREATED)
