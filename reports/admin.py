from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import IncomeReport
from django.utils.html import format_html

# Register your models here.

class IncomeReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'generated_by', 'total_income', 'number_of_payments', 'start_date', 'end_date', 'created_at',)
    search_fields = ('name', 'notes')
    list_filter = ('start_date', 'end_date')

admin.site.register(IncomeReport, IncomeReportAdmin)

# Admin Dashboard View
def custom_admin_dashboard(request):
    reports = IncomeReport.objects.all()  # You can include other reports here as well.
    return render(request, 'admin/custom_dashboard.html', {
        'reports': reports,
    })

class CustomAdminSite(admin.AdminSite):
    site_header = "Property Management System Admin"
    site_title = "Admin Dashboard"
    index_title = "Welcome to the Admin Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom-dashboard/', self.admin_view(custom_admin_dashboard), name='custom_admin_dashboard'),
        ]
        return custom_urls + urls

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        app_list.append({
            'name': 'Reports',
            'app_label': 'reports',
            'models': [
                {
                    'name': 'Income Reports',
                    'url': '/admin/reports/income_report/'
                },
            ]
        })
        return app_list

# Register the custom admin site
admin_site = CustomAdminSite(name='custom_admin')

