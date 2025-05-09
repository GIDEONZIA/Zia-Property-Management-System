# reports/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('income/', views.income_report_view, name='income_report'),
    path('expense/', views.expense_report_view, name='expense_report'),
    path('occupancy/', views.occupancy_report_view, name='occupancy_report'),
    path('maintenance/', views.maintenance_report_view, name='maintenance_report'),
    path('agent-performance/', views.agent_performance_report_view, name='agent_performance_report'),
]
