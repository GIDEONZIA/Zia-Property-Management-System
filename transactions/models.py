from django.db import models
from django.conf import settings
from django.utils import timezone
from properties.models import Property, Tenant, Agent

class Transaction(models.Model):
    PAYMENT = 'Payment'
    CHARGE = 'Charge'
    REFUND = 'Refund'

    TRANSACTION_TYPES = [
        (PAYMENT, 'Payment'),
        (CHARGE, 'Charge'),
        (REFUND, 'Refund'),
    ]

    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]

    CURRENCY_CHOICES = [
        ('KES', 'Kenyan Shilling'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('TSH','Tsh'),
        ('UGX','Ugandan Shilling'),
        ('RWF','Rwandan Franc'),
        ('ZAR','South African Rand'),
        ('TZS','Tanzanian Shilling'),
        ('KWD','Kuwaiti Dinar'),
        ('AED','United Arab Emirates Dirham'),
        ('CAD','Canadian Dollar'),
        ('AUD','Australian Dollar'),
        ('NZD','New Zealand Dollar'),
        ('CHF','Swiss Franc'),
        ('JPY','Japanese Yen'),
        ('CNY','Chinese Yuan'),
        ('INR','Indian Rupee'),
        ('SGD','Singapore Dollar'),
        ('MYR','Malaysian Ringgit'),
        ('THB','Thai Baht'),
        ('PHP','Philippine Peso'),
        ('IDR','Indonesian Rupiah'),
        ('BRL','Brazilian Real'),
        ('MXN','Mexican Peso'),
        ('ARS','Argentine Peso'),
        ('CLP','Chilean Peso'),
        ('COP','Colombian Peso'),
        ('PEN','Peruvian Sol'),  # 🏦 currency field
        # Add more currencies if needed
    ]
    agent = models.ForeignKey(Agent, related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)  # New field for linking transaction to an agent
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default=PAYMENT)
    tenant = models.ForeignKey(Tenant, related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    property = models.ForeignKey(Property, related_name='transactions', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='KES')  # 🏦 currency field
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} {self.currency} - {self.status}"

    class Meta:
        ordering = ['-id']

    def save(self, *args, **kwargs):
        # Ensure that transactions can only be associated with properties that belong to the agent
        if self.agent and self.property and self.property.agent != self.agent:
            raise ValueError("This transaction cannot be associated with a property managed by another agent.")
        super().save(*args, **kwargs)



class MpesaTransaction(models.Model):
    phone_numder = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_reference = models.CharField(max_length=100, unique=True)
    checkout_request_id = models.CharField(max_length=100)
    merchant_request_id = models.CharField(max_length=100)
    result_code = models.IntegerField()
    statues = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mpesa_reference} - {self.status}"