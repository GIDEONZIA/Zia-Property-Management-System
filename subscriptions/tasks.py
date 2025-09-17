from .models import PremiumSubscription, MpesaAuditLog
from django.utils import timezone
from datetime import timedelta

def process_mpesa_callback(data):
    try:
        body = data.get("Body", {})
        stk_callback = body.get("stkCallback", {})
        result_code = stk_callback.get("ResultCode")
        checkout_request_id = stk_callback.get("CheckoutRequestID")
        metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])

        phone = None
        amount = None
        receipt = None

        for item in metadata:
            name = item.get("Name")
            if name == "PhoneNumber":
                phone = str(item.get("Value"))
            elif name == "Amount":
                amount = item.get("Value")
            elif name == "MpesaReceiptNumber":
                receipt = item.get("Value")

        if result_code == 0:  # ✅ Payment successful
            # Log transaction
            MpesaAuditLog.objects.create(
                phone_number=phone,
                amount=amount,
                transaction_type="STK Push",
                reference=receipt,
                status="Success",
                raw_response=data
            )

            # Update subscription
            sub = PremiumSubscription.objects.filter(
                checkout_request_id=checkout_request_id,
                paid=False
            ).last()

            if sub:
                sub.activate(receipt)
        else:
            # ❌ Payment failed
            MpesaAuditLog.objects.create(
                phone_number=phone or "unknown",
                amount=amount or 0,
                transaction_type="STK Push",
                reference=receipt or "N/A",
                status="Failed",
                raw_response=data
            )

    except Exception as e:
        print("⚠️ Mpesa processing error:", e)
