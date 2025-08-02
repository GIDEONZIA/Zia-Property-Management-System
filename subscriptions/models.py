from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


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
    mpesa_receipt = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.phone} - {self.plan} - {'Paid' if self.paid else 'Pending'}"


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
