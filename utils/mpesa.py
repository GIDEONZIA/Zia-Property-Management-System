# utils/mpesa.py

import base64
import requests
from datetime import datetime
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_access_token():
    """Retrieve access token from Safaricom API."""
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    try:
        response = requests.get(url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.RequestException as e:
        logger.error("Failed to get M-Pesa access token: %s", e)
        return None


def initiate_stk_push(phone_number, amount, account_reference, transaction_desc):
    """
    Initiates an M-Pesa STK Push.
    """
    access_token = get_access_token()
    if not access_token:
        return {"error": "Access token generation failed"}

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    try:
        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        logger.info("✅ STK Push initiated: %s", response.json())
        return response.json()

    except requests.RequestException as e:
        logger.error("❌ STK Push failed: %s", e)
        return {"error": str(e)}
