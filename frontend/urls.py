from django.urls import path, include
from django.views.generic import TemplateView
from .views import (
    signup_view, CustomLoginView, idx_search_view, listings_view, contact_view, thank_you_view
)
from django.contrib.auth import views as auth_views
from properties.views import buyer_lead_view, seller_lead_view
from .views import blog_list_view, blog_detail 
from .views import start_premium_subscription, subscription_status_view
from utils.mpesa_callback import mpesa_callback
from frontend.views import home_view




urlpatterns = [
    # Home / Landing
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='landing_page'),
    # Auth
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Static Pages
    path('about/', TemplateView.as_view(template_name='frontend/about.html'), name='about'),
    path('services/', TemplateView.as_view(template_name='frontend/services.html'), name='services'),
    path('testimonial/', TemplateView.as_view(template_name='frontend/testimonial.html'), name='testimonial'),
    path('blog_detail/', TemplateView.as_view(template_name='frontend/blog_detail.html'), name='blog_detail'),
    path('premium_agent/', TemplateView.as_view(template_name='frontend/premium_agent.html'), name='premium_agent'),


    


    # Dynamic Search & Listings Views
    path('idx_search/', idx_search_view, name='idx_search'),
    path('listings/', listings_view, name='listings'),
    path('contact/', contact_view, name='contact'),
    path('buyer/', buyer_lead_view, name='buy'),
    path('sell/', seller_lead_view, name='sell'),
    path('sign-up/', signup_view, name='signup'),
    path('blog/', blog_list_view, name='blog'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('thank-you', thank_you_view, name='thank_you'),
    path('home/', home_view, name='home'),

    path('subscribe/', start_premium_subscription, name='subscribe'),
    path('subscription/', subscription_status_view, name='subscription_status'),  # optional
    
    path('api/mpesa-callback/', mpesa_callback, name='mpesa_callback'),

    
    # AllAuth (optional)
    path('accounts/', include('allauth.urls')),
]
