import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from subscriptions.models import PremiumSubscription, MpesaAuditLog

# Update these two functions in mpesa_callback.py

def process_mpesa_callback(data):
    try:
        callback = data['Body']['stkCallback']
        result_code = callback['ResultCode']
        checkout_id = callback.get('CheckoutRequestID')
        metadata = callback.get('CallbackMetadata', {}).get('Item', [])

        if result_code == 0:
            receipt = next((i['Value'] for i in metadata if i['Name'] == 'MpesaReceiptNumber'), None)
            
            # Find by checkout_request_id instead of just phone
            subscription = PremiumSubscription.objects.filter(
                checkout_request_id=checkout_id, 
                paid=False
            ).last()

            if subscription:
                # Use the model's activate method to set the expiry date!
                subscription.activate(receipt)
                return {"ResultCode": 0, "ResultDesc": "Success"}
            
        return {"ResultCode": 0, "ResultDesc": "No matching record"}
    except Exception as e:
        return {"ResultCode": 1, "ResultDesc": str(e)}

def log_audit(phone, event_type, payload):
    # Fixed field names: phone_number instead of phone, raw_response instead of payload
    MpesaAuditLog.objects.create(
        phone_number=str(phone),
        transaction_type=event_type,
        amount=0,
        reference="CALLBACK",
        status="Received",
        raw_response=payload 
    )

@csrf_exempt
def mpesa_callback(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        data = json.loads(request.body)
        callback = data['Body']['stkCallback']
        metadata = callback.get('CallbackMetadata', {}).get('Item', [])
        
        # Extract metadata for the audit log
        phone = next((i['Value'] for i in metadata if i['Name'] == 'PhoneNumber'), "0")
        amount = next((i['Value'] for i in metadata if i['Name'] == 'Amount'), 0)
        receipt = next((i['Value'] for i in metadata if i['Name'] == 'MpesaReceiptNumber'), "N/A")
        status = "Success" if callback['ResultCode'] == 0 else "Failed"

        log_audit(phone, 'stk_callback', status, amount, receipt, data)

        response = process_mpesa_callback(data)
        return JsonResponse(response)
    except Exception:
        return JsonResponse({"ResultCode": 1}, status=500)
