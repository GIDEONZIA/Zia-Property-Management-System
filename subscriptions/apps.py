# subscriptions/apps.py

from django.apps import AppConfig

class SubscriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscriptions'

    def ready(self):
        from django_q.models import Schedule
        if not Schedule.objects.filter(name='Daily Payment Reminders').exists():
            Schedule.objects.create(
                func='subscriptions.tasks.send_payment_reminders',
                schedule_type=Schedule.DAILY,
                repeats=-1,
                name='Daily Payment Reminders'
            )
