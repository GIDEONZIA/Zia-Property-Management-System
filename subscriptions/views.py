import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

from .models import PremiumSubscription
from utils.mpesa import initiate_stk_push
from utils.mpesa_callback import process_mpesa_callback, log_audit
from django_q.tasks import async_task


@login_required
def premium_agent_page(request):
    """
    Displays the premium subscription page.
    """
    return render(request, 'subscriptions/premium_agent.html')


@login_required
def subscribe_view(request):
    """
    Initiates M-Pesa STK Push and creates a pending PremiumSubscription.
    """
    if request.method == 'POST':
        phone = request.POST.get('phone')
        plan = request.POST.get('plan')

        if not phone or not plan:
            messages.error(request, "Phone number and plan are required.")
            return redirect('premium-agent-page')

        amount = 29 if plan == 'monthly' else 299
        formatted_phone = '254' + phone[1:] if phone.startswith('0') else phone

        response = initiate_stk_push(formatted_phone, amount)

        if response.get("ResponseCode") == "0":
            PremiumSubscription.objects.create(
                user=request.user,
                phone=formatted_phone,
                plan=plan,
                amount=amount,
                paid=False
            )
            messages.success(request, "✅ STK Push sent. Please complete payment on your phone.")
        else:
            messages.error(request, f"❌ Payment failed: {response.get('errorMessage', 'Unknown error')}")

        return redirect('premium-agent-page')

    return redirect('premium-agent-page')


@csrf_exempt
def mpesa_callback_view(request):
    """
    Receives the M-Pesa callback and triggers async processing.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            log_audit(phone=None, event_type="callback_received", payload=data)

            # Queue async task for processing
            async_task('subscriptions.tasks.process_mpesa_callback', data)

            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Callback received'})
        except Exception as e:
            print("⚠️ M-Pesa Callback Error:", e)
            return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Callback processing failed'})

    return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid request method'})
