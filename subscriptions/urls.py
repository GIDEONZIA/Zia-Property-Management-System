from django.urls import path
from .views import subscribe_view, mpesa_callback_view
from subscriptions.views import premium_agent_page

urlpatterns = [
    path('premium_agent/', premium_agent_page, name='premium-agent-page'),
    path('subscribe/', subscribe_view, name='subscribe'),
    path('mpesa/callback/', mpesa_callback_view, name='mpesa-callback'),
]
