from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import MpesaRentPayment

@staff_member_required
def payment_dashboard(request):
    payments = MpesaRentPayment.objects.all().order_by('-transaction_time')
    
    summary = {
        'total': payments.count(),
        'success': payments.filter(matched_by__in=['phone', 'account_ref', 'amount']).count(),
        'failed': payments.filter(matched_by='unmatched').count(),
        'total_amount': sum(p.amount for p in payments if p.matched_by != 'unmatched'),
    }
    
    unmatched = payments.filter(matched_by='unmatched')[:10]
    
    return render(request, 'frontend/payments/dashboard.html', {
        'payments': payments[:50],
        'summary': summary,
        'unmatched': unmatched,
    })