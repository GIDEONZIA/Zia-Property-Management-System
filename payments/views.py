# payments/views.py

import json
from datetime import datetime
from decimal import Decimal

import africastalking
from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from properties.models import Lease, Property, RentPayment, Tenant
from subscriptions.models import MpesaAuditLog
from utils.mpesa import (
    get_access_token,
    register_c2b_urls,
    simulate_c2b_payment,
)

from .models import MpesaRentPayment, ReceiptLog

# -- Africa's Talking ---------------------------------------------------------

africastalking.initialize(
    username=getattr(settings, "AFRICASTALKING_USERNAME", "sandbox"),
    api_key=getattr(settings, "AFRICASTALKING_API_KEY", ""),
)
sms = africastalking.SMS


def _send_sms(phone, message, sender_id=""):
    """Send SMS via Africa's Talking. Returns (success_bool, response)."""
    try:
        phone = str(phone).strip().replace(" ", "").replace("-", "")
        if phone.startswith("0"):
            phone = "254" + phone[1:]
        if phone.startswith("+"):
            phone = phone[1:]

        response = sms.send(message, [phone], sender_id)
        status = response["SMSMessageData"]["Recipients"][0]["status"]
        return status == "Success", response
    except Exception as exc:
        print(f"[SMS Error] {exc}")
        return False, str(exc)


# -- Helpers ------------------------------------------------------------------

def _log_audit(phone, event_type, status, amount, reference, payload):
    """Persist a C2B audit entry."""
    MpesaAuditLog.objects.create(
        phone_number=str(phone),
        transaction_type=event_type,
        amount=amount,
        reference=reference,
        status=status,
        raw_response=payload,
    )


def _normalize_phone(phone):
    """Normalise a Kenyan phone number to 2547XXXXXXXX."""
    phone = str(phone).strip().replace(" ", "").replace("-", "")
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    if len(phone) == 9 and phone.startswith(("7", "1")):
        phone = "254" + phone
    return phone


def _match_payment(phone, account_reference, amount):
    """
    Try to link an incoming C2B payment to a tenant / lease.
    Matching priority: phone -> account_reference -> exact rent amount.
    """
    normalised = _normalize_phone(phone)
    variants = [
        normalised,
        normalised.replace("254", "0", 1),
        normalised.replace("254", "+254", 1),
        "0" + normalised[-9:],
    ]

    # 1. Phone number
    tenant = Tenant.objects.filter(phone__in=variants, is_active=True).first()
    if tenant:
        lease = (
            Lease.objects.filter(tenant=tenant, is_active=True)
            .select_related("property", "agent")
            .first()
        )
        if lease:
            return {
                "tenant": tenant,
                "lease": lease,
                "property": lease.property,
                "agent": lease.agent,
                "matched_by": "phone",
            }

    # 2. Account reference (expected to be the Lease PK)
    if account_reference:
        try:
            lease_id = int(
                account_reference.replace("LEASE", "").replace("-", "").strip()
            )
            lease = (
                Lease.objects.filter(id=lease_id, is_active=True)
                .select_related("tenant", "property", "agent")
                .first()
            )
            if lease:
                return {
                    "tenant": lease.tenant,
                    "lease": lease,
                    "property": lease.property,
                    "agent": lease.agent,
                    "matched_by": "account_ref",
                }
        except (ValueError, TypeError):
            pass

    # 3. Exact rent amount (weakest heuristic)
    try:
        amount_decimal = Decimal(str(amount))
        lease = (
            Lease.objects.filter(rent_amount=amount_decimal, is_active=True)
            .select_related("tenant", "property", "agent")
            .first()
        )
        if lease:
            return {
                "tenant": lease.tenant,
                "lease": lease,
                "property": lease.property,
                "agent": lease.agent,
                "matched_by": "amount",
            }
    except Exception:
        pass

    return {
        "tenant": None,
        "lease": None,
        "property": None,
        "agent": None,
        "matched_by": "unmatched",
    }


def _create_rent_payment_record(mpesa_payment):
    """Mirror the M-Pesa payment in the legacy RentPayment table + update Lease."""
    if not mpesa_payment.lease or not mpesa_payment.tenant:
        return None

    rent_payment = RentPayment.objects.create(
        tenant=mpesa_payment.tenant,
        lease=mpesa_payment.lease,
        amount_paid=mpesa_payment.amount,
        currency="KES",
        payment_method="mpesa",
        receipt_number=f"ZIA-{mpesa_payment.mpesa_receipt_number}",
    )

    lease = mpesa_payment.lease
    lease.is_rent_paid = True
    lease.rent_payment_date = timezone.now()
    lease.rent_payment_status = "completed"
    lease.rent_payment_method = "mpesa"
    lease.rent_payment_reference_number = mpesa_payment.mpesa_receipt_number
    lease.save()

    return rent_payment


# -- Webhooks -----------------------------------------------------------------

@csrf_exempt
def c2b_confirmation(request):
    """
    Safaricom C2B Confirmation endpoint.
    POST /payments/c2b/confirm/
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid JSON"})

    trans_id = data.get("TransID")
    phone = data.get("MSISDN")
    amount = data.get("TransAmount")
    account_ref = data.get("BillRefNumber", "")
    trans_time_str = data.get("TransTime")
    trans_type = data.get("TransactionType", "Pay Bill")
    payer_name = f"{data.get('FirstName', '')} {data.get('LastName', '')}".strip()

    try:
        trans_time = (
            datetime.strptime(trans_time_str, "%Y%m%d%H%M%S")
            if trans_time_str
            else timezone.now()
        )
    except ValueError:
        trans_time = timezone.now()

    _log_audit(
        phone=phone,
        event_type="c2b_confirmation",
        status="Success",
        amount=amount,
        reference=trans_id,
        payload=data,
    )

    if MpesaRentPayment.objects.filter(mpesa_receipt_number=trans_id).exists():
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Duplicate accepted"})

    match = _match_payment(phone, account_ref, amount)

    mpesa_payment = MpesaRentPayment.objects.create(
        tenant=match["tenant"],
        lease=match["lease"],
        property=match["property"],
        agent=match["agent"],
        mpesa_receipt_number=trans_id,
        phone_number=_normalize_phone(phone),
        amount=amount,
        account_reference=account_ref,
        transaction_type=trans_type,
        transaction_time=trans_time,
        payer_name=payer_name,
        matched_by=match["matched_by"],
        notes=f"From {payer_name}" if payer_name else "",
    )

    if match["lease"] and match["tenant"]:
        rent_payment = _create_rent_payment_record(mpesa_payment)
        mpesa_payment.linked_rent_payment = rent_payment
        mpesa_payment.lease_rent_updated = True
        mpesa_payment.save()

    _send_tenant_receipt(mpesa_payment)
    if match["agent"]:
        _notify_agent(mpesa_payment)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})


@csrf_exempt
def c2b_validation(request):
    """
    Safaricom C2B Validation endpoint (called *before* the payment is processed).
    POST /payments/c2b/validate/
    """
    try:
        json.loads(request.body)
    except json.JSONDecodeError:
        pass
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})


# -- Notifications ------------------------------------------------------------

def _send_tenant_receipt(payment):
    """SMS + e-mail receipt to the tenant who paid."""
    if not payment.phone_number:
        return False

    tenant_name = payment.get_tenant_name()
    property_name = payment.get_property_name()
    amount = f"{payment.amount:,.2f}"
    receipt = payment.mpesa_receipt_number
    date_str = payment.transaction_time.strftime("%d %b %Y, %H:%M")

    message = (
        f"Dear {tenant_name}, we received KES {amount} for {property_name}. "
        f"Receipt: {receipt}. Date: {date_str}. Thank you! - Zia PM"
    )

    # SMS
    success, response = _send_sms(payment.phone_number, message)
    ReceiptLog.objects.create(
        payment=payment,
        recipient_type="tenant",
        channel="sms",
        recipient=payment.phone_number,
        message=message,
        status="sent" if success else "failed",
        provider_response=str(response),
    )
    if success:
        payment.tenant_sms_sent = True
        payment.tenant_sms_sent_at = timezone.now()
        payment.save()
        print(f"[OK] SMS sent to tenant {payment.phone_number}")
    else:
        print(f"[FAIL] SMS to tenant {payment.phone_number}: {response}")

    # E-mail
    if payment.tenant and payment.tenant.email:
        from django.core.mail import send_mail

        send_mail(
            subject=f"Rent Payment Receipt - {receipt}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[payment.tenant.email],
            fail_silently=True,
        )
        ReceiptLog.objects.create(
            payment=payment,
            recipient_type="tenant",
            channel="email",
            recipient=payment.tenant.email,
            message=message,
            status="sent",
        )
        payment.tenant_email_sent = True
        payment.tenant_email_sent_at = timezone.now()
        payment.save()
        print(f"[OK] E-mail sent to tenant {payment.tenant.email}")

    return success


def _notify_agent(payment):
    """SMS + e-mail alert to the landlord / agent."""
    if not payment.agent:
        return False

    agent_phone = payment.agent.phone_number
    if not agent_phone:
        return False

    tenant_name = payment.get_tenant_name()
    property_name = payment.get_property_name()
    amount = f"{payment.amount:,.2f}"
    receipt = payment.mpesa_receipt_number

    message = (
        f"Rent Alert: {tenant_name} paid KES {amount} for {property_name}. "
        f"Receipt: {receipt}. - Zia PM"
    )

    # SMS
    success, response = _send_sms(agent_phone, message)
    ReceiptLog.objects.create(
        payment=payment,
        recipient_type="agent",
        channel="sms",
        recipient=agent_phone,
        message=message,
        status="sent" if success else "failed",
        provider_response=str(response),
    )
    if success:
        payment.agent_sms_sent = True
        payment.agent_sms_sent_at = timezone.now()
        payment.save()
        print(f"[OK] SMS sent to agent {agent_phone}")
    else:
        print(f"[FAIL] SMS to agent {agent_phone}: {response}")

    # E-mail
    if payment.agent.email:
        from django.core.mail import send_mail

        send_mail(
            subject=f"Rent Received - {property_name}",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[payment.agent.email],
            fail_silently=True,
        )
        ReceiptLog.objects.create(
            payment=payment,
            recipient_type="agent",
            channel="email",
            recipient=payment.agent.email,
            message=message,
            status="sent",
        )
        payment.agent_email_sent = True
        payment.agent_email_sent_at = timezone.now()
        payment.save()
        print(f"[OK] E-mail sent to agent {payment.agent.email}")

    return success


# -- Admin helpers ------------------------------------------------------------

def register_c2b_view(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Forbidden"}, status=403)
    return JsonResponse(register_c2b_urls())


def simulate_payment_view(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Forbidden"}, status=403)

    phone = request.GET.get("phone", "254708374149")
    amount = request.GET.get("amount", "15000")
    ref = request.GET.get("ref", "LEASE-1")

    return JsonResponse(simulate_c2b_payment(phone, amount, ref))