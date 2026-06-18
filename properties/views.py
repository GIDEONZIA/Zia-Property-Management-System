from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db.models import Count
from django.db.models.functions import TruncMonth
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import (
    BlogPost, Tenant, Lease, MaintenanceRequest, Inspection
)
from properties.models import Property, RentPayment
from properties.serializers import (
    PropertySerializer, TenantSerializer, LeaseSerializer, RentPaymentSerializer
)
from .forms import (
    BuyerLeadForm, SellerLeadForm, LeaseForm, TenantForm, RentPaymentForm
)

class InternalLoginView(LoginView):
    template_name = 'properties/internal_login.html'

    def get_success_url(self):
        return '/dashboard/'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'property_count': Property.objects.count(),
            'tenant_count': Tenant.objects.count(),
            'lease_count': Lease.objects.count(),
            'rent_payment_count': RentPayment.objects.count(),
            'maintenance_request_count': MaintenanceRequest.objects.count(),
            'inspection_count': Inspection.objects.count(),
        })

        leases_by_month = (Lease.objects.annotate(month=TruncMonth('start_date'))
                           .values('month').annotate(count=Count('id')).order_by('month'))
        context["lease_chart_labels"] = [entry["month"].strftime("%b %Y") for entry in leases_by_month]
        context["lease_chart_data"] = [entry["count"] for entry in leases_by_month]

        status_counts = MaintenanceRequest.objects.values('status').annotate(count=Count('id'))
        context["maintenance_labels"] = [item["status"] for item in status_counts]
        context["maintenance_data"] = [item["count"] for item in status_counts]

        return context


@login_required
def tenant_dashboard_view(request):
    tenants = Tenant.objects.filter(agent=request.user.agent_profile) if hasattr(request.user, 'agent_profile') else Tenant.objects.all()
    return render(request, 'properties/tenants.html', {'tenants': tenants})


@login_required
def admin_dashboard(request):
    return render(request, 'properties/admin_dashboard.html', {
        'properties': Property.objects.all(),
        'tenants': Tenant.objects.all(),
        'leases': Lease.objects.all(),
    })

@login_required
def analytics_view(request):
    context = {
        'gross_lease_count': Lease.objects.filter(lease_type='gross').count(),
        'net_lease_count': Lease.objects.filter(lease_type='net').count(),
        'modified_gross_lease_count': Lease.objects.filter(lease_type='modified_gross').count(),
        'triple_net_lease_count': Lease.objects.filter(lease_type='triple_net').count(),
    }
    return render(request, 'properties/analytics.html', context)


class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return Property.objects.all() if self.request.user.is_superuser else Property.objects.filter(agent__user=self.request.user)


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    fields = ['property_name', 'address', 'description', 'property_type', 'location', 'price', 'image']
    template_name = 'properties/property_form.html'
    success_url = '/properties/'

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.is_featured = False
        form.instance.agent = self.request.user.agent_profile
        return super().form_valid(form)


class PropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class TenantListCreateView(generics.ListCreateAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tenant.objects.all() if self.request.user.is_superuser else Tenant.objects.filter(agent__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent_profile)


class TenantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tenant.objects.all() if self.request.user.is_superuser else Tenant.objects.filter(agent__user=self.request.user)


class LeaseListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Lease.objects.all()
        elif hasattr(self.request.user, 'agent_profile'):
            return Lease.objects.filter(agent=self.request.user.agent_profile)
        return Lease.objects.none()

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'agent_profile'):
            raise PermissionDenied("Only agents can create leases.")
        serializer.save(agent=self.request.user.agent_profile)


class LeaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lease.objects.all() if self.request.user.is_superuser else Lease.objects.filter(agent__user=self.request.user)


class RentPaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = RentPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RentPayment.objects.all() if self.request.user.is_superuser else RentPayment.objects.filter(agent__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent_profile)


class RentPaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RentPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RentPayment.objects.all() if self.request.user.is_superuser else RentPayment.objects.filter(agent__user=self.request.user)


@login_required
def buyer_lead_view(request):
    form = BuyerLeadForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Thank you for your interest! We’ll get back to you.")
        return redirect('thank_you')
    return render(request, 'frontend/buyer.html', {'form': form})


@login_required
def seller_lead_view(request):
    form = SellerLeadForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Your property info has been submitted. Our agent will contact you.")
        return redirect('sell')
    return render(request, 'frontend/seller.html', {'form': form})


@login_required
def create_lease_view(request):
    form = LeaseForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        lease = form.save(commit=False)
        if hasattr(request.user, 'agent_profile'):
            lease.agent = request.user.agent_profile
        lease.save()
        return redirect('dashboard')
    return render(request, 'properties/create_lease.html', {'form': form})


@login_required
def lease_list_view(request):
    user = request.user
    leases = Lease.objects.all() if user.is_superuser else Lease.objects.filter(agent=user.agent_profile)
    return render(request, 'properties/lease_list.html', {'leases': leases})


@login_required
def tenant_list_view(request):
    user = request.user
    tenants = Tenant.objects.all() if user.is_superuser else Tenant.objects.filter(agent=user.agent_profile)
    return render(request, 'properties/tenant_list.html', {'tenants': tenants})


@login_required
def create_tenant_view(request):
    form = TenantForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        tenant = form.save(commit=False)
        tenant.agent = request.user.agent_profile
        tenant.save()
        return redirect('tenant_list')
    return render(request, 'properties/create_tenant.html', {'form': form})


@login_required
def create_rent_payment_view(request):
    form = RentPaymentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        rent_payment = form.save(commit=False)
        if hasattr(request.user, 'agent_profile'):
            rent_payment.agent = request.user.agent_profile
        rent_payment.save()
        messages.success(request, "✅ Rent payment recorded successfully.")
        return redirect('dashboard')
    return render(request, 'properties/rent_payment_form.html', {'form': form})


@login_required
def maintenance_request_list_view(request):
    requests = MaintenanceRequest.objects.all() if request.user.is_superuser else MaintenanceRequest.objects.filter(agent=request.user.agent_profile)
    return render(request, 'properties/maintenance_list.html', {'requests': requests})


@login_required
def inspection_list_view(request):
    inspections = Inspection.objects.all()
    return render(request, 'properties/inspection_list.html', {'inspections': inspections})


@login_required
def settings_view(request):
    return render(request, 'properties/settings.html')


@login_required
def update_account_settings(request):
    if request.method == 'POST':
        pass  # Implement settings update logic
    return redirect('settings')


@login_required
def update_notifications(request):
    if request.method == 'POST':
        pass  # Handle notification preference logic
    return redirect('settings')


@login_required
def update_system_settings(request):
    if request.method == 'POST':
        print("System settings form submitted:", request.POST)
    return redirect('settings')


def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'frontend/blog_detail.html', {'blog': blog})
