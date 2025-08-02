from django.db.models.signals import post_save
from django.dispatch import receiver
from subscriptions.models import PremiumSubscription
from django.core.mail import send_mail
from django_q.tasks import async_task

@receiver(post_save, sender=PremiumSubscription)
def notify_agent_after_payment(sender, instance, created, **kwargs):
    if not created and instance.paid and instance.user and instance.user.email:
        send_mail(
            subject="Zia Premium Activated",
            message="Hello Agent,\n\nYour Premium Plan has been successfully activated.",
            from_email="noreply@zia-properties.com",
            recipient_list=[instance.user.email],
        )

@receiver(post_save, sender=PremiumSubscription)
def async_notify_agent(sender, instance, created, **kwargs):
    if not created and instance.paid and instance.user and instance.user.email:
        async_task(send_premium_email, instance.user.email)

def send_premium_email(email):
    from django.core.mail import send_mail
    send_mail(
        subject="Zia Premium Activated",
        message="Your premium subscription is active.",
        from_email="noreply@zia-properties.com",
        recipient_list=[email],
    )
