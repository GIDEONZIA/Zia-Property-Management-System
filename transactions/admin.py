# transactions/admin.py

from django.contrib import admin
from .models import Transaction

# Filter transactions by related property's agent
def filter_agent_queryset(request, qs):
    if request.user.is_superuser:
        return qs
    if hasattr(request.user, 'agent_profile'):
        return qs.filter(property__agent=request.user.agent_profile)
    return qs.none()

class AgentRestrictedAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_agent_queryset(request, qs)

# Transaction Admin
@admin.register(Transaction)
class TransactionAdmin(AgentRestrictedAdmin):
    list_display = ('transaction_type', 'tenant', 'property', 'amount', 'currency', 'status', 'date')
    list_filter = ('transaction_type', 'status', 'currency')
    search_fields = ('tenant__name', 'property__name', 'amount')
    date_hierarchy = 'date'
    ordering = ('-date',)
    actions = ['mark_as_completed']

    @admin.action(description="Mark selected transactions as Completed")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='Completed')
        self.message_user(request, f"{updated} transaction(s) marked as completed.")
