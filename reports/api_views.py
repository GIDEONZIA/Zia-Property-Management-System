"""DRF API views for reports."""
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from properties.models import Agent, Property, Tenant, Lease, RentPayment, MaintenanceRequest


class AgentPerformanceReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agents = Agent.objects.all()
        report = []
        for agent in agents:
            properties = Property.objects.filter(agent=agent)
            tenants = Tenant.objects.filter(agent=agent)
            leases = Lease.objects.filter(agent=agent)
            payments = RentPayment.objects.filter(lease__agent=agent)
            maintenance = MaintenanceRequest.objects.filter(property__agent=agent)

            this_month = timezone.now().replace(day=1, hour=0, minute=0, second=0)
            monthly_revenue = payments.filter(payment_date__gte=this_month).aggregate(
                total=Sum('amount_paid')
            )['total'] or 0

            total_revenue = payments.aggregate(total=Sum('amount_paid'))['total'] or 0
            total_properties = properties.count()
            active_leases = leases.filter(is_active=True).count()
            occupancy = round((active_leases / max(total_properties, 1)) * 100, 1)

            report.append({
                'agent_id': agent.id,
                'first_name': agent.first_name,
                'last_name': agent.last_name,
                'agency_name': agent.agency_name or f"{agent.first_name} {agent.last_name}",
                'email': agent.email,
                'phone_number': agent.phone_number,
                'total_properties': total_properties,
                'total_tenants': tenants.count(),
                'total_leases': leases.count(),
                'active_leases': active_leases,
                'total_revenue': float(total_revenue),
                'monthly_revenue': float(monthly_revenue),
                'occupancy_rate': occupancy,
                'pending_maintenance': maintenance.filter(status='pending').count(),
                'commission_rate': float(agent.commission_rate or 0),
                'is_premium': agent.is_premium,
                'currency': 'KES',
            })
        return Response(report)


class SystemHealthAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.db import connection
        try:
            connection.ensure_connection()
            db_status = 'ok'
        except Exception:
            db_status = 'fail'

        return Response({
            'status': 'ok' if db_status == 'ok' else 'degraded',
            'database': db_status,
            'timestamp': timezone.now().isoformat(),
        })


class MpesaStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.conf import settings
        try:
            from utils.mpesa import get_access_token
            token = get_access_token()
            status = 'ok' if token else 'fail'
        except Exception as e:
            status = f'fail: {str(e)}'

        return Response({
            'mpesa_api_status': status,
            'base_url': getattr(settings, 'MPESA_BASE_URL', 'not_set'),
            'timestamp': timezone.now().isoformat(),
        })


class LastBackupAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'last_backup': None,
            'note': 'Configure backup monitoring in your backup provider',
            'timestamp': timezone.now().isoformat(),
        })


class FailedLoginsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        since = request.query_params.get('since')
        return Response({
            'failed_attempts_last_hour': 0,
            'note': 'Integrate django-axes for real failed login tracking',
            'since': since,
        })
