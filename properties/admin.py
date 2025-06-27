from django.contrib import admin
from .models import (
    BuyerLead, SellerLead, Property, Tenant, Lease,
    RentPayment, PropertyImage, Agent, BlogPost
)

# Admin Panel Branding
admin.site.site_header = "Zia Property Management"
admin.site.site_title = "Zia Property Admin"
admin.site.index_title = "Welcome to Zia Management Portal"

# Utility: Filter queryset per agent
def filter_agent_queryset(request, qs):
    if request.user.is_superuser:
        return qs
    if hasattr(request.user, 'agent_profile'):
        model = qs.model
        if model.__name__ == "Property":
            return qs.filter(agent=request.user.agent_profile)
        elif model.__name__ == "Tenant":
            return qs.filter(agent=request.user.agent_profile)
        elif model.__name__ == "Lease":
            return qs.filter(property__agent=request.user.agent_profile)
        elif model.__name__ == "RentPayment":
            return qs.filter(lease__property__agent=request.user.agent_profile)
    return qs.none()

# Base admin class with agent restriction
class AgentRestrictedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return filter_agent_queryset(request, super().get_queryset(request))

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(request.user, 'agent_profile'):
            if hasattr(obj, 'agent') and not obj.agent:
                obj.agent = request.user.agent_profile
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "agent":
                kwargs["queryset"] = Agent.objects.filter(user=request.user)
            elif db_field.name == "property":
                kwargs["queryset"] = Property.objects.filter(agent=request.user.agent_profile)
            elif db_field.name == "tenant":
                kwargs["queryset"] = Tenant.objects.filter(agent=request.user.agent_profile)
            elif db_field.name == "lease":
                kwargs["queryset"] = Lease.objects.filter(property__agent=request.user.agent_profile)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Property Admin
@admin.register(Property)
class PropertyAdmin(AgentRestrictedAdmin):
    list_display = ('property_name', 'property_type', 'price', 'is_available', 'created_at')
    search_fields = ('property_name', 'address', 'location')
    list_filter = ('property_type', 'is_available')

# Tenant Admin
@admin.register(Tenant)
class TenantAdmin(AgentRestrictedAdmin):
    list_display = ('property_name', 'email', 'phone', 'is_active', 'created_at')
    search_fields = ('property_name', 'email', 'phone')
    list_filter = ('is_active',)

# Lease Admin
@admin.register(Lease)
class LeaseAdmin(AgentRestrictedAdmin):
    list_display = (
        'tenant_name', 'property_name', 'start_date', 'end_date',
        'rent_amount', 'stamp_duty', 'commission_amount_display',
        'total_cost_display', 'is_active'
    )
    search_fields = ('tenant__property_name', 'property__property_name')
    list_filter = ('is_active', 'is_signed', 'is_renewed')

    def tenant_name(self, obj):
        return obj.tenant.property_name

    def property_name(self, obj):
        return obj.property.property_name

    def commission_amount_display(self, obj):
        try:
            return f"{obj.commission_amount():.2f}"
        except Exception:
            return "N/A"
    commission_amount_display.short_description = 'Commission Amount'

    def total_cost_display(self, obj):
        try:
            return f"{obj.total_cost():.2f}"
        except Exception:
            return "N/A"
    total_cost_display.short_description = 'Total Cost'

# RentPayment Admin
@admin.register(RentPayment)
class RentPaymentAdmin(AgentRestrictedAdmin):
    list_display = ('tenant', 'lease', 'amount_paid', 'payment_date')
    search_fields = ('tenant__property_name', 'lease__property__property_name')
    list_filter = ('payment_method',)

# PropertyImage Admin
@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'description')
    search_fields = ('property__property_name',)

# Agent Admin
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'commission_rate', 'is_active', 'is_premium')
    search_fields = ('first_name', 'last_name', 'email')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs if request.user.is_superuser else qs.none()

# BuyerLead Admin
@admin.register(BuyerLead)
class BuyerLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'preferred_location', 'budget', 'created_at')
    search_fields = ('name', 'email', 'phone', 'preferred_location')
    list_filter = ('preferred_location',)

# SellerLead Admin
@admin.register(SellerLead)
class SellerLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'property_type', 'location', 'asking_price', 'created_at')
    search_fields = ('name', 'email', 'phone', 'location', 'property_type')
    list_filter = ('property_type',)

# Blog Admin
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
