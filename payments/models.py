# payments/models.py

from django.db import models
from django.utils import timezone
from properties.models import Tenant, Lease, Property, Agent


class MpesaRentPayment(models.Model):
    """
    Auto-captured rent payments from M-Pesa C2B.
    Separate from your manual RentPayment model to avoid conflicts.
    """
    
    # Links to your existing models
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mpesa_payments'
    )
    lease = models.ForeignKey(
        Lease,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mpesa_payments'
    )
    property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # M-Pesa data
    mpesa_receipt_number = models.CharField(max_length=50, unique=True, db_index=True)
    phone_number = models.CharField(max_length=15, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    account_reference = models.CharField(max_length=50, blank=True, db_index=True)
    transaction_type = models.CharField(max_length=20, default="Pay Bill")
    transaction_time = models.DateTimeField()
    payer_name = models.CharField(max_length=255, blank=True)
    
    # Matching
    MATCHED_BY_CHOICES = [
        ('phone', 'Phone Number'),
        ('account_ref', 'Account Reference'),
        ('amount', 'Amount Match'),
        ('manual', 'Manual Match'),
        ('unmatched', 'Unmatched'),
    ]
    matched_by = models.CharField(
        max_length=20,
        choices=MATCHED_BY_CHOICES,
        default='unmatched'
    )
    
    # Receipt status
    tenant_sms_sent = models.BooleanField(default=False)
    tenant_sms_sent_at = models.DateTimeField(null=True, blank=True)
    tenant_email_sent = models.BooleanField(default=False)
    tenant_email_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Agent/Landlord notification
    agent_sms_sent = models.BooleanField(default=False)
    agent_sms_sent_at = models.DateTimeField(null=True, blank=True)
    agent_email_sent = models.BooleanField(default=False)
    agent_email_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Sync with existing RentPayment model
    linked_rent_payment = models.ForeignKey(
        'properties.RentPayment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mpesa_source'
    )
    
    # Also update Lease rent status
    lease_rent_updated = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-transaction_time']
        verbose_name = "M-Pesa Rent Payment"
        verbose_name_plural = "M-Pesa Rent Payments"
    
    def __str__(self):
        return f"{self.mpesa_receipt_number} - KES {self.amount}"
    
    def get_tenant_name(self):
        if self.tenant:
            return self.tenant.property_name
        return "Unknown Tenant"
    
    def get_property_name(self):
        if self.property:
            return self.property.property_name
        if self.lease:
            return self.lease.property.property_name
        return "Unknown Property"


class ReceiptLog(models.Model):
    """Audit trail for every receipt/notification sent"""
    
    payment = models.ForeignKey(
        MpesaRentPayment,
        on_delete=models.CASCADE,
        related_name='receipt_logs'
    )
    recipient_type = models.CharField(
        max_length=20,
        choices=[
            ('tenant', 'Tenant'),
            ('agent', 'Agent/Landlord'),
        ]
    )
    channel = models.CharField(
        max_length=10,
        choices=[
            ('sms', 'SMS'),
            ('email', 'Email'),
        ]
    )
    recipient = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('failed', 'Failed'),
            ('delivered', 'Delivered'),
        ],
        default='pending'
    )
    provider_response = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.channel} to {self.recipient_type}: {self.status}"