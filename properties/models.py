# properties/models.py

from django.db import models
from django.contrib.auth.models import User

# === GLOBAL CHOICES ===
PROPERTY_TYPES = [
    ('house', 'House'),
    ('apartment', 'Apartment'),
    ('commercial', 'Commercial'),
    ('land', 'Land'),
    ('office', 'Office'),
    ('warehouse', 'Warehouse'),
    ('retail', 'Retail'),
]

PAYMENT_FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('annually', 'Annually'),
]

PAYMENT_METHOD_CHOICES = [
    ('bank_transfer', 'Bank Transfer'),
    ('cash', 'Cash'),
    ('credit_card', 'Credit Card'),
    ('mobile_money', 'Mobile Money'),
    ('mpesa', 'M-Pesa'),
]

RENT_PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
]

# === MODELS ===

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='agents/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)

    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.property.name}"


class Tenant(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='tenants', null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Lease(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    lease_terms = models.TextField()
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY_CHOICES)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    is_active = models.BooleanField(default=True)
    is_signed = models.BooleanField(default=False)
    signed_date = models.DateTimeField(blank=True, null=True)

    # Renewal
    is_renewed = models.BooleanField(default=False)
    renewal_date = models.DateTimeField(blank=True, null=True)
    renewal_terms = models.TextField(blank=True, null=True)
    renewal_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    renewal_fee_paid = models.BooleanField(default=False)
    renewal_fee_paid_date = models.DateTimeField(blank=True, null=True)

    # Termination
    is_terminated = models.BooleanField(default=False)
    termination_date = models.DateTimeField(blank=True, null=True)
    termination_reason = models.TextField(blank=True, null=True)
    termination_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    termination_fee_paid = models.BooleanField(default=False)
    termination_fee_paid_date = models.DateTimeField(blank=True, null=True)
    is_terminated_by_tenant = models.BooleanField(default=False)
    is_terminated_by_landlord = models.BooleanField(default=False)
    termination_notice_period = models.IntegerField(default=30, help_text="Notice period in days")

    # Rent Payment
    is_rent_paid = models.BooleanField(default=False)
    rent_payment_date = models.DateTimeField(blank=True, null=True)
    rent_payment_receipt = models.FileField(upload_to='rent_payment_receipts/', blank=True, null=True)
    rent_payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    rent_payment_reference_number = models.CharField(max_length=50, blank=True, null=True)
    rent_payment_status = models.CharField(max_length=20, choices=RENT_PAYMENT_STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lease: {self.tenant.name} - {self.property.name}"


class RentPayment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    receipt_number = models.CharField(max_length=50, unique=True)
    rent_payment_receipt = models.FileField(upload_to='rent_payment_receipts/', blank=True, null=True)

    def __str__(self):
        return f"Rent Payment by {self.tenant.name} for {self.amount_paid}"

