import csv
from django.http import HttpResponse
from django.contrib import admin
from django_q.models import Task, Schedule

from .models import PremiumSubscription, MpesaAuditLog


@admin.register(PremiumSubscription)
class PremiumSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('phone', 'plan', 'amount', 'paid', 'created_at', 'expiry_date', 'payment_gateway')
    list_filter = ('plan', 'paid', 'payment_gateway')
    search_fields = ('phone', 'mpesa_receipt')
    actions = ['export_paid_subscriptions']

    def export_paid_subscriptions(self, request, queryset):
        paid_subs = queryset.filter(paid=True)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="paid_subscriptions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Phone', 'Plan', 'Amount', 'Receipt', 'Date'])
        for sub in paid_subs:
            writer.writerow([sub.phone, sub.plan, sub.amount, sub.mpesa_receipt, sub.created_at])
        return response

    export_paid_subscriptions.short_description = "Export Paid Subscriptions as CSV"


@admin.register(MpesaAuditLog)
class MpesaAuditLogAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'amount', 'transaction_type', 'reference', 'status', 'created_at')
    list_filter = ('transaction_type', 'status')
    search_fields = ('phone_number', 'reference')


# Unregister Django-Q defaults (may not exist yet, so try/except)
try:
    admin.site.unregister(Task)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(Schedule)
except admin.sites.NotRegistered:
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'func', 'started', 'success', 'attempt_count']
    list_filter = ['success', 'started']
    search_fields = ['name', 'func']
    readonly_fields = ['id', 'name', 'func', 'hook', 'args', 'kwargs', 'result',
                       'started', 'stopped', 'success', 'attempt_count', 'group', 'cluster']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def add_view(self, request, form_url='', extra_context=None):
        from django.contrib import messages
        from django.http import HttpResponseRedirect
        from django.urls import reverse
        
        messages.warning(request, "Tasks cannot be created via admin. Use async_task() or Schedule instead.")
        return HttpResponseRedirect(reverse('admin:django_q_task_changelist'))


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['name', 'func', 'schedule_type', 'next_run', 'repeats']
    list_filter = ['schedule_type']
    search_fields = ['name', 'func']