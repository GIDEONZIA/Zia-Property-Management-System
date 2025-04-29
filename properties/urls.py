from django.urls import path
from . import views
from .views import PropertyListView, PropertyCreateView, PropertyRetrieveUpdateDestroyView
from .views import TenantListCreateView, TenantRetrieveUpdateDestroyView
from .views import LeaseListCreateView, LeaseRetrieveUpdateDestroyView
from .views import RentPaymentListCreateView, RentPaymentRetrieveUpdateDestroyView

urlpatterns = [
    # Agent URLs
    path('agent_properties/', views.agent_properties, name='agent_properties'),
    
      # Property URLs
    path('properties/', PropertyListView.as_view(), name='property-list'),
    path('properties/create/', PropertyCreateView.as_view(), name='property-create'),
    path('properties/<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view(), name='property-detail'),

    # Tenant URLs
    path('tenants/', TenantListCreateView.as_view(), name='tenant-list-create'),
    path('tenants/<int:pk>/', TenantRetrieveUpdateDestroyView.as_view(), name='tenant-detail'),

    # Lease URLs
    path('leases/', LeaseListCreateView.as_view(), name='lease-list-create'),
    path('leases/<int:pk>/', LeaseRetrieveUpdateDestroyView.as_view(), name='lease-detail'),

    # Rent Payment URLs
    path('rent-payments/', RentPaymentListCreateView.as_view(), name='rent-payment-list-create'),
    path('rent-payments/<int:pk>/', RentPaymentRetrieveUpdateDestroyView.as_view(), name='rent-payment-detail'),
]
