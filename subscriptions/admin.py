import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import PremiumSubscription, MpesaAuditLog
from django_q.models import Task


@admin.register(PremiumSubscription)
class PremiumSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('phone', 'plan', 'amount', 'paid', 'created_at','expiry_date', 'payment_gateway')
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


admin.site.register(Task)


@admin.register(MpesaAuditLog)
class MpesaAuditLogAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'amount', 'transaction_type', 'reference', 'status', 'created_at')
    list_filter = ('transaction_type', 'status')
    search_fields = ('phone_number', 'reference')
