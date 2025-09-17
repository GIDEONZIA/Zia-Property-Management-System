from django.shortcuts import redirect
from django.utils import timezone
from .models import PremiumSubscription


class PremiumRequiredMiddleware:
    """
    Middleware that restricts access to premium pages
    unless the user has an active subscription.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip checks for staff/superuser/admin
        if request.user.is_authenticated and not request.user.is_superuser:
            premium_paths = [
                "/premium/",        # example premium dashboard
                "/properties/add/", # maybe posting requires premium
            ]

            # Check if request path is in premium area
            if any(request.path.startswith(p) for p in premium_paths):
                # Look for active subscription
                active_sub = PremiumSubscription.objects.filter(
                    user=request.user,
                    paid=True,
                    expiry_date__gt=timezone.now()
                ).last()

                if not active_sub:
                    return redirect("premium-agent-page")  # 🚀 force subscription page

        return self.get_response(request)
