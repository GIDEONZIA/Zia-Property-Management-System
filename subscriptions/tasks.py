# subscriptions/tasks.py

from django_q.tasks import async_task
from .models import PremiumSubscription

def process_mpesa_callback(data):
    # Parse the M-Pesa data and update subscription
    pass

def send_payment_reminders():
    unpaid = PremiumSubscription.objects.filter(paid=False)
    for sub in unpaid:
        # send email or SMS here
        pass
