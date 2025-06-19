from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import Property, Tenant, Lease, RentPayment

class CustomAdminSite(admin.AdminSite):
    site_header = "Property Management System"
    site_title = "PMS Admin"
    index_title = "Welcome to Zia Property Management System"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.dashboard), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard(self, request):
        context = dict(
            self.each_context(request),
            total_properties=Property.objects.count(),
            total_tenants=Tenant.objects.count(),
            active_leases=Lease.objects.filter(is_active=True).count(),
            total_rent_payments=RentPayment.objects.count(),
        )
        return TemplateResponse(request, "admin/dashboard.html", context)
