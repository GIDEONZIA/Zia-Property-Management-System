from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


class PremiumSubscription(models.Model):
    PLAN_CHOICES = [
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=15)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    mpesa_receipt = models.CharField(max_length=100, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    payment_gateway = models.CharField(max_length=50, default='MPESA')


    def __str__(self):
        return f"{self.phone} - {self.plan} - {'Paid' if self.paid else 'Pending'}"

    def activate(self, receipt):
        """Mark subscription as paid and set expiry date."""
        self.paid = True
        self.mpesa_receipt = receipt
        if self.plan == 'monthly':
            self.expiry_date = timezone.now() + timedelta(days=30)
        elif self.plan == 'annual':
            self.expiry_date = timezone.now() + timedelta(days=365)
        self.save()

    def is_active(self):
        """Check if subscription is still valid."""
        return self.paid and self.expiry_date and self.expiry_date > timezone.now()

class MpesaAuditLog(models.Model):
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    reference = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    raw_response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.reference}"
