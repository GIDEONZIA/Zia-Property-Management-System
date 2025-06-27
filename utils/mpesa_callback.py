# utils/mpesa_callback.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            print("✅ M-Pesa Callback received:", data)

            # Optionally log or save the data
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            print("❌ Error in callback:", e)
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'message': 'Only POST requests allowed'}, status=405)
