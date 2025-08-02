
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from rest_framework_simplejwt import views as jwt_views

from . import views
from .views import (
    PropertyListView, PropertyCreateView, PropertyRetrieveUpdateDestroyView,
    TenantListCreateView, TenantRetrieveUpdateDestroyView,
    LeaseListCreateView, LeaseRetrieveUpdateDestroyView, 
    RentPaymentListCreateView, RentPaymentRetrieveUpdateDestroyView,
    admin_dashboard, agent_dashboard, DashboardView, analytics_view,
    tenant_dashboard_view, lease_list_view, create_lease_view,
    tenant_list_view, maintenance_request_list_view, inspection_list_view, blog_detail # HTML version
)




urlpatterns = [

    # JWT Auth
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # Authentication
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),

    # Dashboards
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('agent_dashboard/', agent_dashboard, name='agent_dashboard'),
    path('dashboard/tenants/', tenant_dashboard_view, name='tenants'),

    # Property HTML Views
    path('', PropertyListView.as_view(), name='property_list'),
    path('create/', PropertyCreateView.as_view(), name='property_create'),

    # Property DRF API
    path('properties/', PropertyListView.as_view(), name='property-list'),
    path('properties/create/', PropertyCreateView.as_view(), name='property-create'),
    path('properties/<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view(), name='property-detail'),

    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),

    # Tenant HTML View
    path('tenants/', tenant_list_view, name='tenant_list'),
    path('tenants/new/', views.create_tenant_view, name='create-tenant'),

    # Tenant DRF API
    path('tenants/api/', TenantListCreateView.as_view(), name='tenant-list-api'),
    path('tenants/api/<int:pk>/', TenantRetrieveUpdateDestroyView.as_view(), name='tenant-detail-api'),


    # Lease HTML View
    path('leases/', lease_list_view, name='lease-list'),
    path('leases/new/', create_lease_view, name='create_lease'),

    # Lease DRF API
    path('leases/api/', LeaseListCreateView.as_view(), name='lease-list-create'),
    path('leases/api/<int:pk>/', LeaseRetrieveUpdateDestroyView.as_view(), name='lease-detail'),


    # ✅ Rent Payment HTML View
    path('rent-payments/', views.create_rent_payment_view, name='rent-payment-create'),

    # ✅ DRF API views
    path('rent-payments/', RentPaymentListCreateView.as_view(), name='rent-payment-list-api'),
    path('rent-payments/<int:pk>/', RentPaymentRetrieveUpdateDestroyView.as_view(), name='rent-payment-detail-api'),



    # Analytics
    path('analytics/', analytics_view, name='analytics'),
    path('properties/analytics/', TemplateView.as_view(template_name='properties/analytics.html'), name='analytics_static'),

    # Maintenance
    path('maintenance/', maintenance_request_list_view, name='maintenance-list'),
    
    #inspection
    path('inspections/', inspection_list_view, name='inspection-list'),

    # settings
    path('settings/', views.settings_view, name='settings'),
    path('settings/update/', views.update_account_settings, name='update_account_settings'),
    path('settings/notifications/', views.update_notifications, name='update_notifications'),
    path('settings/system/', views.update_system_settings, name='update_system_settings'),

    


]

