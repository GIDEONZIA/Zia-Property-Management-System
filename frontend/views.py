import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomSignupForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from properties.models import Property 
from django.shortcuts import render, get_object_or_404
from properties.models import BlogPost 
from django.shortcuts import render, redirect
from properties.models import AgentSubscription
from utils.mpesa import initiate_stk_push
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse



# sign up

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomSignupForm()
    
    return render(request, 'frontend/sign_up.html', {'form': form})

# login
class CustomLoginView(LoginView):
    template_name = 'frontend/login.html'
    authentication_form = AuthenticationForm

# idx_search

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


# listings

def listings_view(request):
    properties = Property.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'frontend/listings.html', {'properties': properties})



# contacts

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
            return redirect('thank_you')
        except Exception as e:
            messages.error(request, f"Failed to send message: {e}")
            return redirect('contact')
    
    return render(request, 'frontend/contact.html')  # this handles GET





def blog_list_view(request):
    posts = BlogPost.objects.all().order_by('-created_at')  # or whatever field you use
    return render(request, 'frontend/blog.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'frontend/blog_detail.html', {'post': post})

def thank_you_view(request):
    return render(request, 'frontend/thank_you.html')


@login_required(login_url='login')
def start_premium_subscription(request):
    if request.method == 'POST':
        user = request.user

        # ✅ Make sure user is an agent
        if not hasattr(user, 'agent_profile'):
            messages.error(request, "You must be registered as an agent to subscribe.")
            return redirect('premium_agent')

        agent = user.agent_profile

        phone = request.POST.get('phone', '').strip()

        # ✅ Format phone number to international format
        if phone.startswith("07"):
            phone = "254" + phone[1:]
        elif phone.startswith("+254"):
            phone = phone.replace("+", "")
        elif phone.startswith("254 ") or " " in phone:
            phone = phone.replace(" ", "")

        plan = request.POST.get('plan')  # 'monthly' or 'annual'
        amount = 29 if plan == 'monthly' else 299

        # ✅ Initiate STK Push
        response = initiate_stk_push(
            phone_number=phone,
            amount=amount,
            account_reference=str(agent.id),
            transaction_desc='Zia Premium Agent Subscription'
        )

        # ✅ Save or update subscription status
        AgentSubscription.objects.update_or_create(
            agent=agent,
            defaults={
                'plan': plan,
                'payment_method': 'mpesa',
                'is_active': False
            }
        )

        return render(request, 'frontend/mpesa_waiting.html', {'response': response})

    return redirect('premium_agent')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from properties.models import AgentSubscription

@login_required
def subscription_status_view(request):
    user = request.user

    # ✅ Check if the logged-in user has an agent profile
    if hasattr(user, 'agent_profile'):
        agent = user.agent_profile
        try:
            subscription = AgentSubscription.objects.get(agent=agent)
        except AgentSubscription.DoesNotExist:
            subscription = None
    else:
        subscription = None

    return render(request, 'frontend/subscription.html', {'subscription': subscription})


@csrf_exempt
def mpesa_callback(request):
    import json
    data = json.loads(request.body.decode('utf-8'))
    stk_callback = data['Body']['stkCallback']

    MpesaTransaction.objects.create(
        phone_number=stk_callback['CallbackMetadata']['Item'][4]['Value'],  # Example
        amount=stk_callback['CallbackMetadata']['Item'][0]['Value'],
        mpesa_reference=stk_callback['CallbackMetadata']['Item'][1]['Value'],
        checkout_request_id=stk_callback['CheckoutRequestID'],
        merchant_request_id=stk_callback['MerchantRequestID'],
        result_code=stk_callback['ResultCode'],
        result_desc=stk_callback['ResultDesc'],
        status='success' if stk_callback['ResultCode'] == 0 else 'failed',
    )

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})


