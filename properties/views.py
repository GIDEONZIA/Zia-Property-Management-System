from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib import messages

from .models import Tenant, Lease
from properties.models import Property, RentPayment, MaintenanceRequest, Inspection
from properties.serializers import PropertySerializer, TenantSerializer, LeaseSerializer, RentPaymentSerializer
from .forms import BuyerLeadForm, SellerLeadForm
from .forms import LeaseForm
from .forms import TenantForm
from .forms import RentPaymentForm  # make sure this exists



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
def agent_dashboard(request):
    return render(request, 'agent_dashboard.html', {
        'properties': Property.objects.filter(agent=request.user.agent_profile)
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


# --- PROPERTY VIEWS ---
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


# --- TENANT VIEWS ---
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


# --- LEASE VIEWS ---
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


# --- RENT PAYMENT VIEWS ---
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


# --- LEADS ---
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
    if request.method == 'POST':
        form = LeaseForm(request.POST, request.FILES)
        if form.is_valid():
            lease = form.save(commit=False)
            if hasattr(request.user, 'agent_profile'):
                lease.agent = request.user.agent_profile
            lease.save()
            return redirect('dashboard')  # or any other success page
    else:
        form = LeaseForm()
    return render(request, 'properties/create_lease.html', {'form': form})


@login_required
def lease_list_view(request):
    user = request.user
    if user.is_superuser:
        leases = Lease.objects.all()
    elif hasattr(user, 'agent_profile'):
        leases = Lease.objects.filter(agent=user.agent_profile)
    else:
        leases = Lease.objects.none()
        
    return render(request, 'properties/lease_list.html', {'leases': leases})


@login_required
def tenant_list_view(request):
    user = request.user
    if user.is_superuser:
        tenants = Tenant.objects.all()
    elif hasattr(user, 'agent_profile'):
        tenants = Tenant.objects.filter(agent=user.agent_profile)
    else:
        tenants = Tenant.objects.none()

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
    if request.method == 'POST':
        form = RentPaymentForm(request.POST, request.FILES)
        if form.is_valid():
            rent_payment = form.save(commit=False)

            # Set agent only if agent_profile exists
            if hasattr(request.user, 'agent_profile'):
                rent_payment.agent = request.user.agent_profile

            rent_payment.save()
            messages.success(request, "✅ Rent payment recorded successfully.")
            return redirect('dashboard')  # or another page
    else:
        form = RentPaymentForm()

    return render(request, 'properties/rent_payment_form.html', {'form': form})

from .models import MaintenanceRequest

@login_required
def maintenance_request_list_view(request):
    if request.user.is_superuser:
        requests = MaintenanceRequest.objects.all()
    else:
        requests = MaintenanceRequest.objects.filter(agent=request.user.agent_profile)

    return render(request, 'properties/maintenance_list.html', {'requests': requests})

from .models import Inspection

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
        # process settings update logic here
        pass
    return redirect('settings')  # or return to dashboard

@login_required
def update_notifications(request):
    if request.method == 'POST':
        # Handle toggle preferences or notification settings logic
        # Example: request.user.profile.receive_email_notifications = ...
        # request.user.profile.save()
        pass
    return redirect('settings')  # or wherever you want

@login_required
def update_system_settings(request):
    if request.method == 'POST':
        # Handle POSTed form data here
        # For now, you can just print to debug or pass
        print("System settings form submitted:", request.POST)
        return redirect('settings')  # redirect to settings page
    return redirect('settings')