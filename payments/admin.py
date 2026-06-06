# payments/admin.py

from django.contrib import admin
from .models import MpesaRentPayment, ReceiptLog


@admin.register(MpesaRentPayment)
class MpesaRentPaymentAdmin(admin.ModelAdmin):
    list_display = [
        'mpesa_receipt_number', 'get_tenant_name', 'amount',
        'matched_by', 'tenant_sms_sent', 'agent_sms_sent', 'transaction_time'
    ]
    list_filter = ['matched_by', 'tenant_sms_sent', 'agent_sms_sent', 'transaction_time']
    search_fields = ['mpesa_receipt_number', 'phone_number', 'account_reference']
    readonly_fields = ['created_at']
    date_hierarchy = 'transaction_time'


@admin.register(ReceiptLog)
class ReceiptLogAdmin(admin.ModelAdmin):
    list_display = ['payment', 'recipient_type', 'channel', 'recipient', 'status', 'sent_at']
    list_filter = ['recipient_type', 'channel', 'status']