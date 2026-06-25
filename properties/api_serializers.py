"""DRF Serializers for n8n automation API endpoints."""
from rest_framework import serializers
from .models import (
    Agent, AgentSubscription, Property, Tenant, Lease, RentPayment,
    MaintenanceRequest, Inspection, BuyerLead, SellerLead, BlogPost,
    ContactMessage, Payment, PropertyImage
)


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = [
            'id', 'user', 'first_name', 'last_name', 'phone_number', 'email',
            'is_active', 'is_premium', 'subscription_plan', 'subscribed_at',
            'commission_rate', 'commission_amount', 'agency_name',
            'business_reg_no', 'license_no', 'physical_address', 'city', 'country',
            'is_verified', 'verified_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AgentSubscriptionSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(), source='agent', write_only=True
    )

    class Meta:
        model = AgentSubscription
        fields = ['id', 'agent', 'agent_id', 'plan', 'is_active', 'start_date', 'end_date',
                  'payment_method', 'transanction_id', 'verified']


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'agent', 'property_name', 'email', 'phone', 'address',
                  'is_active', 'is_verified', 'created_at', 'updated_at']


class PropertySerializer(serializers.ModelSerializer):
    agent = AgentSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(), source='agent', write_only=True, required=False
    )
    images = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            'id', 'property_name', 'address', 'description', 'property_type',
            'agent', 'agent_id', 'location', 'price', 'currency', 'bedrooms',
            'bathrooms', 'size', 'is_available', 'is_featured', 'created_at',
            'image', 'images'
        ]
        read_only_fields = ['id', 'created_at']


class LeaseSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    tenant_id = serializers.PrimaryKeyRelatedField(
        queryset=Tenant.objects.all(), source='tenant', write_only=True
    )
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source='property', write_only=True
    )
    agent = AgentSerializer(read_only=True)
    agent_id = serializers.PrimaryKeyRelatedField(
        queryset=Agent.objects.all(), source='agent', write_only=True, required=False
    )

    class Meta:
        model = Lease
        fields = [
            'id', 'tenant', 'tenant_id', 'property', 'property_id', 'agent', 'agent_id',
            'lease_type', 'start_date', 'end_date', 'rent_amount', 'currency',
            'lease_terms', 'security_deposit', 'payment_frequency', 'payment_method',
            'is_active', 'is_signed', 'signed_date', 'stamp_duty',
            'is_renewed', 'renewal_date', 'renewal_terms', 'renewal_fee',
            'renewal_fee_paid', 'renewal_fee_paid_date',
            'is_terminated', 'termination_date', 'termination_reason',
            'termination_fee', 'termination_fee_paid', 'termination_fee_paid_date',
            'is_terminated_by_tenant', 'is_terminated_by_landlord',
            'termination_notice_period',
            'is_rent_paid', 'rent_payment_date', 'rent_payment_status',
            'rent_payment_method', 'rent_payment_reference_number',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RentPaymentSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    tenant_id = serializers.PrimaryKeyRelatedField(
        queryset=Tenant.objects.all(), source='tenant', write_only=True
    )
    lease = LeaseSerializer(read_only=True)
    lease_id = serializers.PrimaryKeyRelatedField(
        queryset=Lease.objects.all(), source='lease', write_only=True
    )

    class Meta:
        model = RentPayment
        fields = [
            'id', 'tenant', 'tenant_id', 'lease', 'lease_id',
            'amount_paid', 'currency', 'payment_date', 'payment_method',
            'receipt_number', 'rent_payment_receipt'
        ]


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source='property', write_only=True
    )

    class Meta:
        model = MaintenanceRequest
        fields = ['id', 'property', 'property_id', 'issue', 'status', 'requested_on']
        read_only_fields = ['id', 'requested_on']


class InspectionSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all(), source='property', write_only=True
    )

    class Meta:
        model = Inspection
        fields = ['id', 'property', 'property_id', 'inspection_date', 'inspector_name', 'notes', 'status']


class BuyerLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerLead
        fields = ['id', 'name', 'email', 'phone', 'preferred_location', 'budget', 'currency', 'message', 'created_at']


class SellerLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerLead
        fields = ['id', 'name', 'email', 'phone', 'property_type', 'location', 'asking_price',
                  'estimated_value', 'currency', 'property_location', 'notes', 'message', 'created_at']


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'summary', 'content', 'image', 'author', 'created_at', 'is_published']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'sent_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'tenant', 'amount', 'currency', 'payment_method', 'reference_code', 'date_paid', 'remarks']
