from django.urls import path, include
from django.views.generic import TemplateView
from .views import signup_view, CustomLoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='landing_page'),
    path('login/', auth_views.LoginView.as_view(template_name='frontend/login.html', redirect_authenticated_user=True), name='login'),
    path('home/', TemplateView.as_view(template_name='frontend/home.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='frontend/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),

    path('sign-up/', signup_view, name='signup'),
    path('about/', TemplateView.as_view(template_name='frontend/about.html'), name='about'),
    path('listings/', TemplateView.as_view(template_name='frontend/listings.html'), name='listings'),
    path('contact/', TemplateView.as_view(template_name='frontend/contact.html'), name='contact'),
    path('services/', TemplateView.as_view(template_name='frontend/services.html'), name='services'),
    path('testimonial/', TemplateView.as_view(template_name='frontend/testimonial.html'), name='testimonial'),

    # Add other static routes as needed
    path('accounts/', include('allauth.urls')),

]
