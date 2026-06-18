# properties/models.py

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# === GLOBAL CHOICES ===
PROPERTY_TYPES = [
    ('house', 'House'),
    ('apartment', 'Apartment'),
    ('commercial', 'Commercial'),
    ('resort', 'Resort'),
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

# === Agent Models ===

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    
    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='agents/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Commission
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Commission rate percentage")
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Commission amount earned by the agent for this tenant")
    
    # Status
    is_active = models.BooleanField(default=True)

    # Premium Subscription Fields
    is_premium = models.BooleanField(default=False)
    subscription_plan = models.CharField(
        max_length=20,
        choices=[('monthly', 'Monthly'), ('annual', 'Annual')],
        blank=True,
        null=True
    )
    subscribed_at = models.DateTimeField(null=True, blank=True)
    trial_used = models.BooleanField(default=False)
        # Business Info
    agency_name = models.CharField(max_length=200, blank=True, null=True)
    business_reg_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Business Registration Number")
    license_no = models.CharField(max_length=100, blank=True, null=True, verbose_name="Real Estate License Number")
    
    # Address
    physical_address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True, default="Kenya")
    
    # Verification Documents
    id_document = models.FileField(upload_to='agents/documents/', blank=True, null=True, verbose_name="National ID/Passport")
    business_certificate = models.FileField(upload_to='agents/documents/', blank=True, null=True)
    
    # Agent Type / Role
    AGENT_TYPE_CHOICES = [
        ('independent', 'Independent Agent'),
        ('agency', 'Agency Representative'),
        ('landlord_agent', 'Landlord & Agent'),
        ('tenant_agent', 'Tenant & Agent'),
    ]
    agent_type = models.CharField(max_length=20, choices=AGENT_TYPE_CHOICES, default='independent')
    
    # Experience
    years_of_experience = models.PositiveIntegerField(default=0)
    properties_managed = models.PositiveIntegerField(default=0)
    
    # Verification Status
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
class AgentSubscription(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=[('monthly', 'Monthly'), ('annual', 'Annual')])
    is_active = models.BooleanField(default=False)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50)
    transanction_id = models.CharField(max_length=100, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.agent.user.username} - {self.plan}"



CURRENCY_CHOICES = [
    ('KES', 'Kenyan Shilling'),
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
    ('GBP', 'British Pound'),
    ('TSH','Tanzanian Shilling'),
    ('UGX','Ugandan Shilling'),
    ('RWF','Rwandan Franc'),
    ('ZAR','South African Rand'),

]
class Property(models.Model):
    property_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)  # 🏦 currency field
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='property_images/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)


    def __str__(self):
        return self.property_name

class BuyerLead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_location = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)  # 🏦 currency field 
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SellerLead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='house')
    location = models.CharField(max_length=255, default='unknown')
    asking_price = models.DecimalField(max_digits=12, decimal_places=2, default=1000000)    
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # ✅ Optional field
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=0)  # 🏦 currency field
    property_location = models.CharField(max_length=255, blank=True, null=True)  
    notes = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


User = get_user_model()

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Most recent first
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'





class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.property.property_name}"


class Tenant(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='tenants', null=True, blank=True)
    property_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.property_name


LEASE_TYPE_CHOICES = [
    ('gross', 'Gross Lease'),
    ('net', 'Net Lease'),
    ('modified_gross', 'Modified Gross Lease'),
    ('triple_net', 'Triple Net Lease'),
]

class Lease(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='leases', null=True, blank=True)
    lease_type = models.CharField(max_length=20, choices=LEASE_TYPE_CHOICES, default='gross')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    lease_type = models.CharField(max_length=50, blank=True, null=True, help_text="Type of lease ('gross', 'net', 'modified_gross', 'triple_net')")
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)  # 🏦 currency field
    lease_terms = models.TextField()
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY_CHOICES)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    is_active = models.BooleanField(default=True)
    is_signed = models.BooleanField(default=False)
    signed_date = models.DateTimeField(blank=True, null=True)
    stamp_duty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, help_text="Stamp duty for this lease")

    # Renewal
    is_renewed = models.BooleanField(default=False)
    renewal_date = models.DateTimeField(blank=True, null=True)
    renewal_terms = models.TextField(blank=True, null=True)
    renewal_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)  # 🏦 currency field
    renewal_fee_paid = models.BooleanField(default=False)
    renewal_fee_paid_date = models.DateTimeField(blank=True, null=True)

    # Termination
    is_terminated = models.BooleanField(default=False)
    termination_date = models.DateTimeField(blank=True, null=True)
    termination_reason = models.TextField(blank=True, null=True)
    termination_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)  # 🏦 currency field 
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

    def commission_amount(self):
        Agent = getattr(self.tenant, 'agent', None)
        rate = getattr(Agent, 'commission_rate', None)
        if rate is not None:
            return (self.rent_amount * rate) / Decimal(100)
    
        if self.tenant.agent and self.tenant.agent.commission_rate:
            return (self.rent_amount * self.tenant.agent.commission_rate) / 100
        return 0
    
    def total_cost(self):
        return self.rent_amount + (self.stamp_duty or 0)
    def __str__(self):
        return f"Lease: {self.tenant.property_name} - {self.property.property_name}"


class RentPayment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)  # 🏦 currency field
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES)
    receipt_number = models.CharField(max_length=50, unique=True)
    rent_payment_receipt = models.FileField(upload_to='rent_payment_receipts/', blank=True, null=True)

    def __str__(self):
        return f"Rent Payment by {self.tenant.property_name} for {self.amount_paid}"

# Maintenance Request Model

class MaintenanceRequest(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    issue = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ], default='pending')
    requested_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.property} - {self.status}"

# Inspection Model
class Inspection(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    inspection_date = models.DateField()
    inspector_name = models.CharField(max_length=255)
    notes = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='scheduled')

    def __str__(self):
        return f"{self.property} - {self.inspection_date} - {self.status}"


 # adjust if your Tenant model is elsewhere
class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)  # 🏦 currency field
    payment_method = models.CharField(max_length=50, choices=[
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('bank', 'Bank Transfer'),
        ('card', 'Card Payment'),
    ])
    reference_code = models.CharField(max_length=100, blank=True, null=True)
    date_paid = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tenant.property_name} - KES {self.amount} on {self.date_paid}"

# models.py
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

