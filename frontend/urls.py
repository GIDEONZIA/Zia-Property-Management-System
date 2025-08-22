from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from .views import PrivacyPolicyView, TermsAndConditionsView
from . import views

from .views import (
    signup_view, CustomLoginView, idx_search_view, listings_view, contact_view, thank_you_view,
    blog_list_view, blog_detail, start_premium_subscription, subscription_status_view, home_view
)
from properties.views import buyer_lead_view, seller_lead_view
from utils.mpesa_callback import mpesa_callback
from subscriptions.views import premium_agent_page

app_name = 'frontend'

urlpatterns = [
    # Home / Landing
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='landing_page'),

    # Authentication
    path('login/', CustomLoginView.as_view(), name='login'),  # main login
    path('agent/login/', CustomLoginView.as_view(), name='agent_login'),  # alias for agents
    path('logout/', auth_views.LogoutView.as_view(next_page='frontend:landing_page'), name='logout'),
    path('sign-up/', signup_view, name='signup'),

    # Static Pages
    path('about/', TemplateView.as_view(template_name='frontend/about.html'), name='about'),
    path('services/', TemplateView.as_view(template_name='frontend/services.html'), name='services'),
    path('premium_agent/', TemplateView.as_view(template_name='frontend/premium_agent.html'), name='premium_agent'),

    # Dynamic Search & Listings Views
    path('idx_search/', idx_search_view, name='idx_search'),
    path('listings/', listings_view, name='listings'),
    path('property/<int:pk>/', views.property_detail_view, name='property_detail'),  # ✅ This is the one

    path('contact/', contact_view, name='contact'),
    path('buyer/', buyer_lead_view, name='buy'),
    path('sell/', seller_lead_view, name='sell'),

    # Blog
    path('blog/', blog_list_view, name='blog'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),

    # Thank You Page
    path('thank-you', thank_you_view, name='thank_you'),

    # Dashboard / Home
    path('home/', home_view, name='home'),

    # Subscriptions
    path('subscribe/', start_premium_subscription, name='subscribe'),
    path('subscription/', subscription_status_view, name='subscription_status'),
    path('premium-agent/', premium_agent_page, name='premium-agent-page'),

    # API Callback
    path('api/mpesa-callback/', mpesa_callback, name='mpesa_callback'),

    # AllAuth
    path('accounts/', include('allauth.urls')),

    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms_and_conditions'),
    # ... other URLs

]
