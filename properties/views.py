from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from rest_framework import generics
from properties.models import Property, Tenant, Lease, RentPayment
from rest_framework.permissions import IsAuthenticated
from properties.serializers import PropertySerializer, TenantSerializer, LeaseSerializer, RentPaymentSerializer
from django.shortcuts import render
from .models import Property

def agent_properties_view(request):
    # Get the logged-in agent's profile (assuming `user` has `agent_profile` relationship)
    agent = request.user.agent_profile

    # Filter properties to only show those that belong to the logged-in agent
    properties = Property.objects.filter(agent=agent)

    # Ensure that no other agent's properties are accessible
    if properties.exists():
        return render(request, 'properties/agent_property_list.html', {'properties': properties})
    else:
        return render(request, 'properties/no_properties.html')  # Show a message if no properties

def agent_properties(request):
    # Get the current logged-in agent
    agent = request.user.agent_profile  # Assuming `agent_profile` is the related_name for the OneToOneField
    properties = Property.objects.filter(agent=agent)
    
    return render(request, 'properties/agent_properties.html', {'properties': properties})

# Property Views
class PropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Property.objects.all()  # Admin sees all properties
        # Make sure the agent is linked to the correct `User` through the `Agent` model
        return Property.objects.filter(agent__user=user)  # Agent sees only their own properties

class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    fields = ['name', 'address', 'description', 'property_type', 'location', 'price', 'image']
    template_name = 'properties/property_form.html'
    success_url = '/properties/'

    def form_valid(self, form):
        # Assign the logged-in user as the agent via the Agent model
        form.instance.agent = self.request.user.agent_profile  # Assuming the agent is linked to the user
        return super().form_valid(form)

class PropertyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Property.objects.all()  # Admin sees all properties
        return Property.objects.filter(agent__user=user)  # Agent sees only their own properties

# Tenant Views
class TenantListCreateView(generics.ListCreateAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Tenant.objects.all()  # Admin sees all tenants
        return Tenant.objects.filter(agent__user=user)  # Agent sees only their own tenants

    def perform_create(self, serializer):
        # Associate the tenant with the agent by referencing the logged-in user's agent
        serializer.save(agent=self.request.user.agent_profile)

class TenantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Tenant.objects.all()  # Admin sees all tenants
        return Tenant.objects.filter(agent__user=user)  # Agent sees only their own tenants

# Lease Views
class LeaseListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Lease.objects.all()  # Admin sees all leases
        return Lease.objects.filter(agent__user=user)  # Agent sees only their own leases

    def perform_create(self, serializer):
        # Associate the lease with the logged-in user's agent
        serializer.save(agent=self.request.user.agent_profile)

class LeaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LeaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Lease.objects.all()  # Admin sees all leases
        return Lease.objects.filter(agent__user=user)  # Agent sees only their own leases

# Rent Payment Views
class RentPaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = RentPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RentPayment.objects.all()  # Admin sees all rent payments
        return RentPayment.objects.filter(agent__user=user)  # Agent sees only their own rent payments

    def perform_create(self, serializer):
        # Associate the rent payment with the logged-in user's agent
        serializer.save(agent=self.request.user.agent_profile)

class RentPaymentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RentPaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return RentPayment.objects.all()  # Admin sees all rent payments
        return RentPayment.objects.filter(agent__user=user)  # Agent sees only their own rent payments
