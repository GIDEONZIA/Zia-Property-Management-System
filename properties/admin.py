from django.contrib import admin
from django.urls import path, include

# Customize admin panel
admin.site.site_header = "Zia Property Management"
admin.site.site_title = "Zia Property Management Admin"
admin.site.index_title = "Welcome to Zia Property Management Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('properties.urls')),  # other routes
]

# properties/admin.py

from django.contrib import admin
from .models import Property, Tenant, Lease, RentPayment, PropertyImage, Agent

# Common function
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

# Base Admin
class AgentRestrictedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_agent_queryset(request, qs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if hasattr(request.user, 'agent_profile') and hasattr(obj, 'agent') and not obj.agent:
                obj.agent = request.user.agent_profile
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "agent":
                kwargs["queryset"] = Agent.objects.filter(user=request.user)
            if db_field.name == "property":
                kwargs["queryset"] = Property.objects.filter(agent=request.user.agent_profile)
            if db_field.name == "tenant":
                kwargs["queryset"] = Tenant.objects.filter(agent=request.user.agent_profile)
            if db_field.name == "lease":
                kwargs["queryset"] = Lease.objects.filter(property__agent=request.user.agent_profile)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Property Admin
@admin.register(Property)
class PropertyAdmin(AgentRestrictedAdmin):
    list_display = ('property_name', 'property_type', 'price', 'is_available', 'created_at')
    search_fields = ('property_property_name', 'address', 'location')
    list_filter = ('property_type', 'is_available')

# Tenant Admin
@admin.register(Tenant)
class TenantAdmin(AgentRestrictedAdmin):
    list_display = ('property_name', 'email', 'phone', 'is_active', 'created_at')
    search_fields = ('property_property_name', 'email', 'phone')
    list_filter = ('is_active', 'is_verified')

# Lease Admin
@admin.register(Lease)
class LeaseAdmin(AgentRestrictedAdmin):
    list_display = ('tenant_name',
                    'property_name',
                    'start_date',
                    'end_date',
                    'rent_amount',
                    'stamp_duty',
                    'commission_amount_display',
                    'total_cost_display',
                    'is_active')
    search_fields = ('tenant__property_name', 'property__property_name')
    list_filter = ('is_active',
                   'is_signed',
                   'is_renewed',
                   ('agent', admin.EmptyFieldListFilter),
    )

    def tenant_name(self, obj):
        return obj.tenant.property_name

    def property_name(self, obj):
        return obj.property.property_name
    
    def commission_amount_display(self, obj):
        try:
            return f"{obj.commission_amount():.2f}" 
        except Exception:
            return "N/A"
        finally:
            pass  # Optional: Add cleanup code here if needed
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
    search_fields = ('tenant_property_name', 'lease_property_name')
    list_filter = ('payment_method',)

# PropertyImage Admin
@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'description')
    search_fields = ('property__name',)

# Agent Admin
@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'commission_rate', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.none()

