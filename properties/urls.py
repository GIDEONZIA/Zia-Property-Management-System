
from django.urls import path
from . import views
from .views import PropertyListView, PropertyCreateView, PropertyRetrieveUpdateDestroyView
from .views import TenantListCreateView, TenantRetrieveUpdateDestroyView
from .views import LeaseListCreateView, LeaseRetrieveUpdateDestroyView
from .views import RentPaymentListCreateView, RentPaymentRetrieveUpdateDestroyView
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from .views import admin_dashboard, agent_dashboard
from django.views.generic import TemplateView
from .views import DashboardView
from rest_framework_simplejwt import views as jwt_views  # Import JWT views
from .views import analytics_view
from .views import tenant_dashboard_view


urlpatterns = [
    
     # JWT Authentication endpoints
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get access and refresh tokens
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Refresh the token
  
    # Custom Dashboards
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('agent_dashboard/', agent_dashboard, name='agent_dashboard'),

    # Property URLs
    path('properties/', PropertyListView.as_view(), name='property-list'),
    path('properties/create/', PropertyCreateView.as_view(), name='property-create'),
    path('properties/<int:pk>/', PropertyRetrieveUpdateDestroyView.as_view(), name='property-detail'),

    # Tenant URLs
    path('tenants/', TenantListCreateView.as_view(), name='tenant-list'),
    path('tenants/<int:pk>/', TenantRetrieveUpdateDestroyView.as_view(), name='tenant-detail'),
    path('tenants/', tenant_dashboard_view, name='tenant-list'),  # For the tenants list page

    # Lease URLs
    path('leases/', LeaseListCreateView.as_view(), name='lease-list-create'),
    path('leases/<int:pk>/', LeaseRetrieveUpdateDestroyView.as_view(), name='lease-detail'),

    # Rent Payment URLs
    path('rent-payments/', RentPaymentListCreateView.as_view(), name='rent-payment-list-create'),
    path('rent-payments/<int:pk>/', RentPaymentRetrieveUpdateDestroyView.as_view(), name='rent-payment-detail'),

    # Analytics URLs
    path('properties/analytics/', TemplateView.as_view(template_name='properties/analytics.html'), name='analytics'),
    path ('analytics/', analytics_view, name='analytics'),
    # Authentication URLs
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login/'), name='logout'),
    
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    path('dashboard/tenants/', tenant_dashboard_view, name='tenants'),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    

]
