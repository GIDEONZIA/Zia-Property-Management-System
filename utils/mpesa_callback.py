from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from subscriptions.models import PremiumSubscription, MpesaAuditLog


def process_mpesa_callback(data):
    try:
        callback = data['Body']['stkCallback']
        result_code = callback['ResultCode']
        metadata = callback.get('CallbackMetadata', {}).get('Item', [])

        if result_code == 0:
            phone = next((i['Value'] for i in metadata if i['Name'] == 'PhoneNumber'), None)
            amount = next((i['Value'] for i in metadata if i['Name'] == 'Amount'), None)
            receipt = next((i['Value'] for i in metadata if i['Name'] == 'MpesaReceiptNumber'), None)

            subscription = PremiumSubscription.objects.filter(phone=str(phone), paid=False).last()
            if subscription:
                subscription.paid = True
                subscription.mpesa_receipt = receipt
                subscription.save()

        return {"ResultCode": 0, "ResultDesc": "Processed"}
    except Exception as e:
        print("M-PESA callback processing error:", e)
        return {"ResultCode": 1, "ResultDesc": "Error"}


def log_audit(phone, event_type, payload):
    MpesaAuditLog.objects.create(
        phone=phone,
        event_type=event_type,
        payload=payload
    )


@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Try to get phone number from callback
            phone = ''
            try:
                metadata = data['Body']['stkCallback'].get('CallbackMetadata', {}).get('Item', [])
                phone_item = next((i for i in metadata if i['Name'] == 'PhoneNumber'), None)
                if phone_item:
                    phone = phone_item.get('Value', '')
            except Exception:
                pass

            log_audit(
                phone=phone,
                event_type='stk_callback',
                payload=json.dumps(data)
            )

            response = process_mpesa_callback(data)
            return JsonResponse(response)

        except Exception as e:
            print("Error in mpesa_callback view:", e)
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Failed to process"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=400)
