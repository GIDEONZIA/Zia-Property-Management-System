# subscriptions/views.py
import json
import logging
from django.shortcuts import render, redirect
from django.contrib import messages

from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django_q.tasks import async_task

from .models import PremiumSubscription
from utils.mpesa import initiate_stk_push
from utils.mpesa_callback import log_audit

logger = logging.getLogger(__name__)

# -----------------------
# Classic form-post subscribe (server-side fallback)
# -----------------------
@login_required
def subscribe_view(request):
    """
    Handles a classic form POST (non-JS) to initiate STK push and create a pending subscription.
    """
    if request.method != 'POST':
        return redirect('frontend:premium_agent')

    phone = request.POST.get('phone', '').strip()
    plan = request.POST.get('plan')

    if not phone or not plan:
        messages.error(request, "Phone and plan are required.")
        return redirect('frontend:premium_agent')

    # Normalize phone
    if phone.startswith('0'):
        formatted_phone = '254' + phone[1:]
    elif phone.startswith('+'):
        formatted_phone = phone.replace('+', '')
    else:
        formatted_phone = phone

    amount = 29 if plan.lower() == 'monthly' else 299

    # initiate STK push
    try:
        response = initiate_stk_push(formatted_phone, amount)
    except Exception as e:
        messages.error(request, f"Failed to initiate payment: {e}")
        return redirect('frontend:premium_agent')

    if response.get("ResponseCode") == "0":
        checkout_id = response.get("CheckoutRequestID")
        PremiumSubscription.objects.create(
            user=request.user,
            phone=formatted_phone,
            plan=plan,
            amount=amount,
            paid=False,
            checkout_request_id=checkout_id
        )
        return redirect(f"/mpesa-waiting/?checkout_id={checkout_id}")
    else:
        messages.error(request, f"Payment initiation failed: {response}")

    return redirect('frontend:premium_agent')


# -----------------------
# JS API: initiate STK Push (called from premium_agent.html via fetch)
# -----------------------
@csrf_exempt
def stk_push(request):
    """
    Initiate STK push (JSON). Returns checkout_request_id and status 'pending'.
    Frontend should redirect user to waiting page to poll check_status.
    """
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    phone = payload.get('phone', '').strip()
    plan = payload.get('plan')
    amount_value = payload.get('amount')
    gateway = payload.get('gateway', 'MPESA')

    if not phone or not plan or not amount_value:
        return JsonResponse({"error": "phone, plan and amount are required"}, status=400)

    # Normalize phone formats (support 07xxxx, +2547xxxx, 2547xxxx)
    if phone.startswith('0'):
        formatted_phone = '254' + phone[1:]
    elif phone.startswith('+'):
        formatted_phone = phone.replace('+', '')
    else:
        formatted_phone = phone

    try:
        amount = int(amount_value)
    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid amount"}, status=400)

    # call your existing initiate_stk_push function
    from utils.mpesa import initiate_stk_push
    try:
        response = initiate_stk_push(formatted_phone, amount)
    except Exception as e:
        logger.exception("Failed to call MPesa")
        return JsonResponse({"error": f"Failed to call M-Pesa: {e}"}, status=500)

    checkout_id = response.get('CheckoutRequestID') or response.get('checkout_request_id')
    # persist pending subscription if we have a checkout id and authenticated user
    if checkout_id and request.user.is_authenticated:
        PremiumSubscription.objects.create(
            user=request.user,
            phone=formatted_phone,
            plan=plan,
            amount=amount,
            paid=False,
            payment_gateway=gateway,
            checkout_request_id=checkout_id
        )

    return JsonResponse({
        "status": "pending",
        "checkout_request_id": checkout_id,
        "mpesa_response": response
    })


# -----------------------
# M-Pesa Callback endpoint
# -----------------------
@csrf_exempt
def mpesa_callback_view(request):
    """
    Endpoint to receive M-Pesa callback (from Safaricom). We queue async processing.
    """
    if request.method != 'POST':
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid JSON'}, status=400)

    # Audit/log the incoming callback (use your utils for structured logging)
    try:
        log_audit(phone=None, event_type="callback_received", payload=data)
    except Exception:
        # non-fatal: we still proceed to queue processing
        pass

    # Queue asynchronous task for heavy processing (recommended)
    try:
        async_task('subscriptions.tasks.process_mpesa_callback', data)
    except Exception as e:
        # If async task queuing fails, try immediate processing (fallback)
        try:
            from subscriptions.tasks import process_mpesa_callback as _proc
            _proc(data)
        except Exception as e2:
            # Logging only; return a 200 to M-Pesa to avoid retries if you decide so.
            return JsonResponse({'ResultCode': 1, 'ResultDesc': f'Callback processing failed: {e2}'}, status=500)

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Callback received'})




@csrf_exempt
def check_status(request):
    """
    Polling endpoint that checks M-Pesa payment status by checkout_request_id.
    Returns: { "status": "success" | "failed" | "pending" | "not_found" }
    """
    checkout_id = request.GET.get("checkout_id")
    if not checkout_id:
        return JsonResponse({"status": "error", "message": "Missing checkout_id"}, status=400)

    try:
        sub = PremiumSubscription.objects.filter(checkout_request_id=checkout_id).first()
        if not sub:
            return JsonResponse({"status": "not_found"})

        if sub.paid:
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "pending"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
