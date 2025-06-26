from django.urls import path, include
from django.views.generic import TemplateView
from .views import (
    signup_view, CustomLoginView, idx_search_view, listings_view, contact_view
)
from django.contrib.auth import views as auth_views
from properties.views import buyer_lead_view, seller_lead_view
from frontend.views import blog_list_view, blog_detail


urlpatterns = [
    # Home / Landing
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='landing_page'),
    path('home/', TemplateView.as_view(template_name='frontend/home.html'), name='home'),

    # Auth
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Static Pages
    path('about/', TemplateView.as_view(template_name='frontend/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='frontend/contact.html'), name='contact'),
    path('services/', TemplateView.as_view(template_name='frontend/services.html'), name='services'),
    path('testimonial/', TemplateView.as_view(template_name='frontend/testimonial.html'), name='testimonial'),
    path('blog_detail/', TemplateView.as_view(template_name='frontend/blog_detail.html'), name='blog_detail'),
    path('thank-you/', TemplateView.as_view(template_name='frontend/thank_you.html'), name='thank_you'),


    # Dynamic Search & Listings Views
    path('idx_search/', idx_search_view, name='idx_search'),
    path('listings/', listings_view, name='listings'),
    path('contact/', contact_view, name='contact'),
    path('buyer/', buyer_lead_view, name='buy'),
    path('sell/', seller_lead_view, name='sell'),
    path('sign-up/', signup_view, name='signup'),
    path('blog/', blog_list_view, name='blog'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),


    # AllAuth (optional)
    path('accounts/', include('allauth.urls')),
]
