# reports/admin.py

from django.contrib import admin
from .models import IncomeReport

@admin.register(IncomeReport)
class IncomeReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'generated_by', 'total_income', 'number_of_payments', 'start_date', 'end_date', 'created_at', 'notes')
    search_fields = ('name', 'notes')
    list_filter = ('start_date', 'end_date')

    def save_model(self, request, obj, form, change):
        # Ensure the 'generated_by' field is set to the current user when creating a report
        if not obj.generated_by:
            obj.generated_by = request.user
        super().save_model(request, obj, form, change)
