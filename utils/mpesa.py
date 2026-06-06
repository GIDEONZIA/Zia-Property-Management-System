# utils/mpesa.py

import base64
import requests
from datetime import datetime
from django.conf import settings


def get_access_token():
    """Get M-Pesa OAuth access token"""
    auth = f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
    encoded = base64.b64encode(auth.encode()).decode()
    
    response = requests.get(
        f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {encoded}"}
    )
    
    if response.status_code == 200 :
        return response.json().get("access_token")
    return None


def initiate_stk_push(phone, amount):
    """STK Push for subscription payments — your existing flow"""
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
        f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    return response.json()


# ========== NEW — C2B Support ==========

def register_c2b_urls():
    """
    Register C2B Confirmation & Validation URLs with Safaricom.
    Run this once per environment (sandbox + production).
    """
    access_token = get_access_token()
    if not access_token:
        return {"error": "Could not get access token"}

    # Build C2B URLs from your callback base
    base = settings.MPESA_CALLBACK_URL.rstrip('/')
    # If your callback is https://xxx.ngrok-free.app/subscriptions/callback/
    # C2B URLs will be: https://xxx.ngrok-free.app/payments/c2b/confirm/
    confirmation_url = base.replace('/subscriptions/callback', '/payments/c2b/confirm')
    validation_url = base.replace('/subscriptions/callback', '/payments/c2b/validate')

    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": confirmation_url,
        "ValidationURL": validation_url,
    }

    response = requests.post(
        f"{settings.MPESA_BASE_URL}/mpesa/c2b/v1/registerurl",
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    return response.json()


def simulate_c2b_payment(phone, amount, account_reference="RENT001"):
    """
    TESTING ONLY — Simulate a C2B payment in sandbox.
    In production, real customers pay via M-Pesa menu.
    """
    access_token = get_access_token()
    if not access_token:
        return {"error": "Could not get access token"}

    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "CommandID": "CustomerPayBillOnline",
        "Amount": amount,
        "Msisdn": phone,
        "BillRefNumber": account_reference,
    }

    response = requests.post(
        f"{settings.MPESA_BASE_URL}/mpesa/c2b/v1/simulate",
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )
    return response.json()