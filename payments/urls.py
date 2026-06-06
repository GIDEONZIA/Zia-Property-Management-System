# payments/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # C2B Webhooks
    path('c2b/confirm/', views.c2b_confirmation, name='c2b_confirmation'),
    path('c2b/validate/', views.c2b_validation, name='c2b_validation'),
    
    # Admin tools
    path('admin/register-c2b/', views.register_c2b_view, name='register_c2b'),
    path('admin/simulate/', views.simulate_payment_view, name='simulate_c2b'),
]