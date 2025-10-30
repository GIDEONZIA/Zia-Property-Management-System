from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('stk_push/', views.stk_push, name='stk_push'),
    path('callback/', views.mpesa_callback_view, name='mpesa_callback'),
    path('check-status/', views.check_status, name='check_status'),

]
