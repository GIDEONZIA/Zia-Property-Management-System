# frontend/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    signup_view, PublicLoginView, AgentLoginView, idx_search_view, listings_view,
    contact_view, thank_you_view, blog_list_view, blog_detail, home_view,
    premium_agent_page, payment_success,testimonials_view,
)
from django.views.generic import TemplateView

app_name = 'frontend'

urlpatterns = [
    # Landing / Home
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='landing_page'),
    path('home/', home_view, name='home'),

    # Auth
    path('login/', PublicLoginView.as_view(), name='login'),
    path('agent/login/', AgentLoginView.as_view(), name='agent_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='frontend:landing_page'), name='logout'),
    path('sign-up/', signup_view, name='signup'),

    # Pages
    path('about/', TemplateView.as_view(template_name='frontend/about.html'), name='about'),
    path('services/', TemplateView.as_view(template_name='frontend/services.html'), name='services'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-and-conditions/', views.TermsAndConditionsView.as_view(), name='terms_and_conditions'),
    path('testimonials/', views.testimonials_view, name='testimonials'),


    # Listings & Search
    path('idx_search/', idx_search_view, name='idx_search'),
    path('listings/', listings_view, name='listings'),
    path('property/<int:pk>/', views.property_detail_view, name='property_detail'),

    # Contact & Blog
    path('contact/', contact_view, name='contact'),
    path('thank-you', thank_you_view, name='thank_you'),
    path('blog/', blog_list_view, name='blog'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),

    # Premium (renders the page) and payment success page (frontend only)
    path('premium-agent/', premium_agent_page, name='premium_agent'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('mpesa-waiting/', views.mpesa_waiting, name='mpesa_waiting'),


    # Delegated endpoints (handled by subscriptions app)
    # NOTE: mpesa callback should point to the subscriptions app; do NOT expose internal logic here.
    path('accounts/', include('allauth.urls')),
]
