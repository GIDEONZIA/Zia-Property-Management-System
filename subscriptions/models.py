from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

class PremiumSubscription(models.Model):
    PLAN_CHOICES = [
        ('monthly', 'Monthly (30 Days)'),
        ('annual', 'Annual (365 Days)'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="subscriptions"
    )
    phone = models.CharField(max_length=15)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Use DateTimeField consistently for time-sensitive logic
    expiry_date = models.DateTimeField(blank=True, null=True, db_index=True)
    
    mpesa_receipt = models.CharField(max_length=100, blank=True, null=True, unique=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    payment_gateway = models.CharField(max_length=50, default='MPESA')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Premium Subscription"

    def __str__(self):
        status = "✅ Paid" if self.paid else "⏳ Pending"
        return f"{self.user.username} ({self.plan}) - {status}"

    def activate(self, receipt):
        """Mark as paid and intelligently set expiry date."""
        self.paid = True
        self.mpesa_receipt = receipt
        
        # Logic: If user has an existing active plan, add time to the current expiry
        # instead of starting from "now" (Fair Renewal Logic)
        start_point = timezone.now()
        if self.user.subscriptions.filter(paid=True, expiry_date__gt=timezone.now()).exists():
            last_sub = self.user.subscriptions.filter(paid=True).latest('expiry_date')
            start_point = last_sub.expiry_date

        days = 30 if self.plan == 'monthly' else 365
        self.expiry_date = start_point + timedelta(days=days)
        self.save()

    @property
    def is_active(self):
        """Check if subscription is currently valid."""
        if not self.paid or not self.expiry_date:
            return False
        return self.expiry_date > timezone.now()

    @property
    def days_left(self):
        """Returns number of days remaining."""
        if self.is_active:
            delta = self.expiry_date - timezone.now()
            return delta.days
        return 0

class MpesaAuditLog(models.Model):
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50)
    reference = models.CharField(max_length=100) # Receipt Number
    status = models.CharField(max_length=20)   # Success / Failed
    raw_response = models.JSONField()         # Store the full JSON for debugging
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "M-Pesa Audit Log"
