# frontend/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.utils.http import url_has_allowed_host_and_scheme
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .forms import CustomSignupForm
from properties.models import Property, BlogPost

# -----------------------
# Authentication / Signup
# -----------------------
def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please log in.")
            return redirect('frontend:login')
    else:
        form = CustomSignupForm()
    return render(request, 'frontend/sign_up.html', {'form': form})


class PublicLoginView(LoginView):
    template_name = 'frontend/public_login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, self.request.get_host()):
            return next_url
        return reverse_lazy('frontend:home')


class AgentLoginView(LoginView):
    template_name = 'frontend/agent_login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, self.request.get_host()):
            return next_url
        return reverse_lazy('agent_dashboard')


# -----------------------
# Public / Frontend pages
# -----------------------
def home_view(request):
    featured_properties = Property.objects.filter(is_featured=True, is_available=True).order_by('-created_at')[:3]
    return render(request, 'frontend/home.html', {'featured_properties': featured_properties})


def idx_search_view(request):
    properties = Property.objects.all()
    location = request.GET.get('location')
    type_ = request.GET.get('type')
    price = request.GET.get('price')

    if location:
        properties = properties.filter(location__icontains=location)
    if type_:
        properties = properties.filter(property_type__iexact=type_)
    if price:
        properties = properties.filter(price__lte=price)

    return render(request, 'frontend/idx_search.html', {'properties': properties})


def listings_view(request):
    properties = Property.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'frontend/listings.html', {'properties': properties})


def property_detail_view(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    return render(request, 'frontend/property_detail.html', {'property': property_obj})


def blog_list_view(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'frontend/blog.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'frontend/blog_detail.html', {'post': post})


class PrivacyPolicyView(TemplateView):
    template_name = "frontend/privacy_policy.html"


class TermsAndConditionsView(TemplateView):
    template_name = "frontend/terms_and_conditions.html"


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"From: {name} <{email}>\n\nMessage:\n{message}"

        try:
            send_mail(
                subject="New Contact Message from Zia Website",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['gwiternz@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Message sent successfully.")
            return redirect('frontend:thank_you')
        except Exception as e:
            messages.error(request, f"Failed to send message: {e}")
            return redirect('frontend:contact')

    return render(request, 'frontend/contact.html')


def thank_you_view(request):
    return render(request, 'frontend/thank_you.html')


# -----------------------
# Premium / Payment pages (render only)
# -----------------------
@login_required
def premium_agent_page(request):
    """
    Renders the premium landing page. The actual payment initiation
    is handled by the subscriptions app via the `subscriptions:stk_push` endpoint.
    """
    return render(request, 'frontend/premium_agent.html')


@login_required
def payment_success(request):
    """
    Simple page to show after a successful payment.
    The subscription activation should be handled by the callback that marks a subscription paid.
    """
    return render(request, 'frontend/payment_success.html')


def payment_failed(request):
    """
    Simple page to show after a failed payment.
    """
    return render(request, 'frontend/payment_failed.html')

def mpesa_waiting(request):
    """
    Display the waiting screen while polling payment status.
    """
    checkout_id = request.GET.get("checkout_id")
    return render(request, "frontend/mpesa_waiting.html", {"checkout_id": checkout_id})
