"""API URL router for reports app."""
from django.urls import path
from .api_views import (
    AgentPerformanceReportAPIView, SystemHealthAPIView,
    MpesaStatusAPIView, LastBackupAPIView, FailedLoginsAPIView
)

urlpatterns = [
    path('agent-performance/', AgentPerformanceReportAPIView.as_view(), name='api_agent_performance'),
    path('health/', SystemHealthAPIView.as_view(), name='api_health'),
    path('mpesa-status/', MpesaStatusAPIView.as_view(), name='api_mpesa_status'),
    path('last-backup/', LastBackupAPIView.as_view(), name='api_last_backup'),
    path('failed-logins/', FailedLoginsAPIView.as_view(), name='api_failed_logins'),
]
