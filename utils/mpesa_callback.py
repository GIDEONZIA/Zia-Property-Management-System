# utils/mpesa_callback.py

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
import logging

# Optional: configure a logger for M-Pesa
logger = logging.getLogger(__name__)

@csrf_exempt
def mpesa_callback(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Only POST requests allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        logger.info("✅ M-Pesa Callback received: %s", json.dumps(data, indent=2))

        # Optionally: extract relevant details (safe structure assumed)
        callback = data.get("Body", {}).get("stkCallback", {})
        result_code = callback.get("ResultCode")
        result_desc = callback.get("ResultDesc")

        metadata = callback.get("CallbackMetadata", {}).get("Item", [])
        parsed_data = {item['Name']: item.get('Value') for item in metadata if 'Value' in item}

        # Placeholder to store or process parsed_data
        # Example:
        # phone = parsed_data.get("PhoneNumber")
        # amount = parsed_data.get("Amount")

        # Optional: Log to DB or audit file
        # MpesaTransaction.objects.create(...)

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"}, status=200)

    except Exception as e:
        logger.error("❌ Error in M-Pesa callback: %s", str(e), exc_info=True)
        return JsonResponse({'error': 'Invalid callback structure or processing failed.'}, status=400)
