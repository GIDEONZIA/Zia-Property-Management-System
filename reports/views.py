# reports/views.py

from django.shortcuts import render
from django.db.models import Sum
from properties.models import Payment  # Assuming your app is 'properties'

# View for the Income Report
def income_report_view(request):
    # Aggregate total income from payments in the database
    total_income = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    
    # Query payments with related tenant data, ordered by the date they were paid
    payments = Payment.objects.select_related('tenant').order_by('-date_paid')

    return render(request, 'reports/income_report.html', {
        'title': 'Income Report',
        'total_income': total_income,
        'payments': payments,
    })

# View for the Report Dashboard
def report_dashboard(request):
    return render(request, 'reports/dashboard.html')

# Views for other reports (rendering empty templates for now)
def expense_report_view(request):
    return render(request, 'reports/expense_report.html')

def occupancy_report_view(request):
    return render(request, 'reports/occupancy_report.html')

def maintenance_report_view(request):
    return render(request, 'reports/maintenance_report.html')

def agent_performance_report_view(request):
    return render(request, 'reports/agent_performance_report.html')
