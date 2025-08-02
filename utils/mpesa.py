# subscriptions/utils/mpesa.py

import base64
import requests
from datetime import datetime
from django.conf import settings

def get_access_token():
    auth = f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
    encoded = base64.b64encode(auth.encode()).decode()
    response = requests.get(
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {encoded}"}
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def initiate_stk_push(phone, amount):
    access_token = get_access_token()
    if not access_token:
        return {"errorMessage": "Access token error"}

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        (settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()
    ).decode()

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": "ZiaPremium",
        "TransactionDesc": "Premium Agent Subscription"
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    return response.json()
