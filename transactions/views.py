from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Transaction, Tenant, Property
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def create_transaction(request):
    if request.method == 'POST':
        tenant = Tenant.objects.get(user=request.user)
        property = tenant.property
        transaction_type = request.POST.get('transaction_type')
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')

        transaction = Transaction.objects.create(
            tenant=tenant,
            property=property,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
        )
        return redirect('transactions:transaction_list')

    return render(request, 'transactions/create_transaction.html')


@login_required
def transaction_list(request):
    tenant = Tenant.objects.get(user=request.user)
    transactions = Transaction.objects.filter(tenant=tenant).order_by('-date')
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})


@login_required
def update_transaction_status(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        transaction.status = status
        transaction.save()
        return redirect('transactions:transaction_list')
    return render(request, 'transactions/update_transaction_status.html', {'transaction': transaction})
