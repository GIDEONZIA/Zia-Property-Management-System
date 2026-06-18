from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
from .views import (
    signup_view, PublicLoginView, AgentLoginView, idx_search_view, listings_view,
    contact_view, thank_you_view, blog_list_view, blog_detail, home_view,
    premium_agent_page, payment_success, testimonials_view, agent_register_view,
    agent_dashboard_view, agent_properties_view, agent_property_detail_view,
    agent_tenants_view, agent_leases_view, agent_payments_view,
    agent_maintenance_view, agent_inspections_view, agent_analytics_view,
    agent_settings_view,
    agent_property_create_view, agent_tenant_create_view, agent_lease_create_view,
    agent_maintenance_create_view, agent_inspection_create_view,
)

app_name = 'frontend'

urlpatterns = [
    # Landing / Home
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='landing_page'),
    path('home/', views.home_view, name='home'),

    # Auth
    path('login/', views.PublicLoginView.as_view(), name='login'),
    path('agent/login/', views.AgentLoginView.as_view(), name='agent_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='frontend:landing_page'), name='logout'),
    path('sign-up/', views.signup_view, name='signup'),
    path('register-agent/', views.agent_register_view, name='agent_register'),

    # Agent Portal
    path('agent/dashboard/', views.agent_dashboard_view, name='agent_dashboard'),
    path('agent/properties/', views.agent_properties_view, name='agent_properties'),
    path('agent/properties/add/', views.agent_property_create_view, name='agent_property_add'),
    path('agent/properties/<int:pk>/', views.agent_property_detail_view, name='agent_property_detail'),
    path('agent/tenants/', views.agent_tenants_view, name='agent_tenants'),
    path('agent/tenants/add/', views.agent_tenant_create_view, name='agent_tenant_add'),
    path('agent/leases/', views.agent_leases_view, name='agent_leases'),
    path('agent/leases/create/', views.agent_lease_create_view, name='agent_lease_create'),
    path('agent/payments/', views.agent_payments_view, name='agent_payments'),
    path('agent/maintenance/', views.agent_maintenance_view, name='agent_maintenance'),
    path('agent/maintenance/new/', views.agent_maintenance_create_view, name='agent_maintenance_new'),
    path('agent/inspections/', views.agent_inspections_view, name='agent_inspections'),
    path('agent/inspections/schedule/', views.agent_inspection_create_view, name='agent_inspection_schedule'),
    path('agent/analytics/', views.agent_analytics_view, name='agent_analytics'),
    path('agent/settings/', views.agent_settings_view, name='agent_settings'),
    
    # Pages
    path('about/', TemplateView.as_view(template_name='frontend/about.html'), name='about'),
    path('services/', TemplateView.as_view(template_name='frontend/services.html'), name='services'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-and-conditions/', views.TermsAndConditionsView.as_view(), name='terms_and_conditions'),
    path('testimonials/', views.testimonials_view, name='testimonials'),

    # Listings & Search
    path('idx_search/', views.idx_search_view, name='idx_search'),
    path('listings/', views.listings_view, name='listings'),
    path('property/<int:pk>/', views.property_detail_view, name='property_detail'),

    # Contact & Blog
    path('contact/', views.contact_view, name='contact'),
    path('thank-you', views.thank_you_view, name='thank_you'),
    path('blog/', views.blog_list_view, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    # Premium & Payments
    path('premium-agent/', views.premium_agent_page, name='premium_agent'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('mpesa-waiting/', views.mpesa_waiting, name='mpesa_waiting'),

    # Allauth
    path('accounts/', include('allauth.urls')),
]