from django.apps import AppConfig
from django.db.models.signals import post_migrate

class SubscriptionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "subscriptions"

    def ready(self):
        from django_q.models import Schedule
        from django.db.utils import OperationalError, ProgrammingError

        def create_schedule(sender, **kwargs):
            try:
                Schedule.objects.get_or_create(
                    name="Daily Payment Reminders",
                    defaults={"func": "subscriptions.tasks.send_reminders", "schedule_type": "D"}
                )
            except (OperationalError, ProgrammingError):
                # Database not ready yet
                pass

        post_migrate.connect(create_schedule, sender=self)
