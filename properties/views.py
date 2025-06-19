from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from rest_framework import generics
from properties.models import Property, Tenant, Lease, RentPayment, MaintenanceRequest, Inspection
from rest_framework.permissions import IsAuthenticated
from properties.serializers import PropertySerializer, TenantSerializer, LeaseSerializer, RentPaymentSerializer
from django.shortcuts import render
from .models import Tenant, Lease
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count, Sum


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_count'] = Property.objects.all()
        context['tenant_count'] = Tenant.objects.all()
        context['lease_count'] = Lease.objects.all()
        context['rent_payment_count'] = RentPayment.objects.all()
        context['maintenance_request_count'] = MaintenanceRequest.objects.all()
        context['inspection_count'] = Inspection.objects.all()
        
        # Leases per month
        leases_by_month = (
            Lease.objects.annotate(month=TruncMonth('start_date'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        
        context["lease_chart_labels"] = [entry["month"].strftime("%b %Y") for entry in leases_by_month]
        context["lease_chart_data"] = [entry["count"] for entry in leases_by_month]
        
        status_counts = (
            MaintenanceRequest.objects.values('status')
            .annotate(count=Count('id'))
        )
        
        context["maintenance_labels"] = [item["status"] for item in status_counts]
        context["maintenance_data"] = [item["count"] for item in status_counts]
        return context

def tenant_dashboard_view(request):
    user = request.user
    if hasattr(user, 'agent'):
        tenants = Tenant.objects.filter(agent=user.agent)
    else:
        tenants = Tenant.objects.all()  # superuser or admin
    return render(request, 'properties/tenants.html', {'tenants': tenants})

# Dashboard Views
def admin_dashboard(request):
    properties = Property.objects.all()
    tenants = Tenant.objects.all()
    leases = Lease.objects.all()
    return render(request, 'properties/admin_dashboard.html', {'properties': properties, 'tenants': tenants}) 

def agent_dashboard(request):
    agent = request.user
    properties = Property.objects.filter(agent=agent)
    return render(request, 'agent_dashboard.html', {'properties': properties})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def dashboard_view(request):
    # Fetch live data from the models
    property_count = Property.objects.count()
    lease_count = Lease.objects.count()
    tenants_count = Tenant.objects.count()
    maintenance_request_count = MaintenanceRequest.objects.count()
    rent_payment_count = RentPayment.objects.count()

    return render(request, 'dashboard.html', {
        'property_count': property_count,
        'lease_count': lease_count,
        'tenants_count': tenants_count,
        'rent_payment_count': rent_payment_count,
        'maintenance_request_count': maintenance_request_count,
    })
    
# Login View
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_staff:
            return '/admin_dashboard/'
        return '/agent_dashboard/'
    
@login_required
def analytics_view(request):
    gross_lease_count = Lease.objects.filter(lease_type='gross').count()
    net_lease_count = Lease.objects.filter(lease_type='net').count()
    modified_gross_lease_count = Lease.objects.filter(lease_type='modified_gross').count()
    triple_net_lease_count = Lease.objects.filter(lease_type='triple_net').count()

    # Include in context:
    context = {
        'gross_lease_count': gross_lease_count,
        'net_lease_count': net_lease_count,
        'modified_gross_lease_count': modified_gross_lease_count,
        'triple_net_lease_count': triple_net_lease_count,
        # Existing context values
    }

    return render(request, 'properties/analytics.html', context)
# Property Views
class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Property.objects.all()
        return Property.objects.filter(agent__user=user)

class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    fields = ['name', 'address', 'description', 'property_type', 'location', 'price', 'image']
    template_name = 'properties/property_form.html'
    success_url = '/properties/'

    def form_valid(self, form):
        form.instance.agent = self.request.user.agent_profile
        return super().form_valid(form)

class PropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Property.objects.all()
        return Property.objects.filter(agent__user=user)

# Tenant Views
class TenantListCreateView(generics.ListCreateAPIView):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Tenant.objects.all()
        return Tenant.objects.filter(agent__user=user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent_profile)
        
    def get(self, request, *args, **kwargs):
        tenants = self.get_queryset()  # Get the list of tenants
        return render(request, 'properties/tenants.html', {'tenants': tenants})

# properties/views.py

def tenant_list_view(request):
    tenants = Tenant.objects.all()
    # Optionally filter based on user permissions (similar to your API view)
    user = request.user
    if not user.is_superuser:
        tenants = tenants.filter(agent__user=user)
    
    return render(request, 'properties/tenants.html', {'tenants': tenants})

class TenantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Tenant.objects.all()
        return Tenant.objects.filter(agent__user=user)

# Lease Views
class LeaseListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Lease.objects.all()
        return Lease.objects.filter(agent__user=user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent_profile)

class LeaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Lease.objects.all()
        return Lease.objects.filter(agent__user=user)

# Rent Payment Views
class RentPaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = RentPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RentPayment.objects.all()
        return RentPayment.objects.filter(agent__user=user)

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent_profile)

class RentPaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RentPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RentPayment.objects.all()
        return RentPayment.objects.filter(agent__user=user)
