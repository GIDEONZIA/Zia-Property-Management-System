from .models import PremiumSubscription, MpesaAuditLog
from django.db import transaction
import logging
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
# It's better to use a logger than 'print' in production
logger = logging.getLogger(__name__)

def process_mpesa_callback(data):
    try:
        # 1. Extract the core data from the Safaricom JSON
        body = data.get("Body", {})
        stk_callback = body.get("stkCallback", {})
        result_code = stk_callback.get("ResultCode")
        checkout_request_id = stk_callback.get("CheckoutRequestID")
        metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])

        phone = None
        amount = None
        receipt = None

        # 2. Parse the metadata list
        for item in metadata:
            name = item.get("Name")
            value = item.get("Value")
            if name == "PhoneNumber":
                phone = str(value)
            elif name == "Amount":
                amount = value
            elif name == "MpesaReceiptNumber":
                receipt = value

        # 3. Handle the Payment Logic
        if result_code == 0:  # ✅ Payment successful
            with transaction.atomic():
                # Log the success in the Audit table
                MpesaAuditLog.objects.create(
                    phone_number=phone,
                    amount=amount,
                    transaction_type="STK Push",
                    reference=receipt,
                    status="Success",
                    raw_response=data
                )

                # Find and activate the matching subscription
                # select_for_update() locks the row so two callbacks don't process at once
                sub = PremiumSubscription.objects.filter(
                    checkout_request_id=checkout_request_id,
                    paid=False
                ).select_for_update().last()

                if sub:
                    sub.activate(receipt)
                else:
                    logger.warning(f"⚠️ Subscription not found for ID: {checkout_request_id}")
        
        else:  # ❌ Payment failed (User cancelled or insufficient funds)
            MpesaAuditLog.objects.create(
                phone_number=phone or "unknown",
                amount=amount or 0,
                transaction_type="STK Push",
                reference=receipt or "N/A",
                status="Failed",
                raw_response=data
            )

    except Exception as e:
        # This 'except' fixes the SyntaxError you were seeing
        logger.error(f"⚠️ Mpesa processing error: {e}")


def send_reminders():
    """
    Scheduled task to remind users whose subscriptions are expiring soon.
    Runs daily via Django Q.
    """
    reminder_date = timezone.now().date() + timedelta(days=3)
    
    # Find paid subscriptions expiring on that specific date
    expiring_soon = PremiumSubscription.objects.filter(
        expiry_date=reminder_date,
        paid=True
    )

    sent_count = 0

    for sub in expiring_soon:
        try:
            send_mail(
                subject="Your Premium Subscription is Expiring Soon!",
                message=f"Hi {sub.user.username}, your subscription expires on {sub.expiry_date}. Renew now to stay premium!",
                from_email="noreply@ziaproperties.com",
                recipient_list=[sub.user.email],
                fail_silently=False,
            )
            sent_count += 1
        except Exception as e:
            logger.error(f"❌ Failed to send reminder to {sub.user.email}: {e}")

    return f"Successfully sent {sent_count} reminders for {reminder_date}"
