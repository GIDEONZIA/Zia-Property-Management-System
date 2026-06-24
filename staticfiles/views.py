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
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta

from testimonial.models import Testimonial
from .forms import CustomSignupForm, AgentSignupForm
from properties.models import Property, BlogPost, Agent, Tenant, Lease, RentPayment, MaintenanceRequest, Inspection


# ==================== AUTHENTICATION ====================

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


def agent_register_view(request):
    if request.method == 'POST':
        form = AgentSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                "Agent account created successfully! Your profile is pending verification. You can now log in."
            )
            return redirect('frontend:agent_login')
    else:
        form = AgentSignupForm()
    return render(request, 'frontend/agent_register.html', {'form': form})


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
        return reverse_lazy('frontend:agent_dashboard')


# ==================== AGENT PORTAL ====================

def get_agent_or_redirect(request):
    """Helper to get agent profile or redirect to home."""
    try:
        return request.user.agent_profile
    except Agent.DoesNotExist:
        messages.error(request, "You don't have an agent profile.")
        return None


@login_required
def agent_dashboard_view(request):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    # Properties
    agent_properties = Property.objects.filter(agent=agent)
    total_properties = agent_properties.count()
    available_properties = agent_properties.filter(is_available=True).count()

    # Tenants
    agent_tenants = Tenant.objects.filter(agent=agent)
    total_tenants = agent_tenants.count()
    new_tenants_this_month = agent_tenants.filter(
        created_at__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0)
    ).count()

    # Leases
    agent_leases = Lease.objects.filter(agent=agent)
    total_leases = agent_leases.count()
    active_leases = agent_leases.filter(is_active=True).count()
    leases_ending_soon = agent_leases.filter(
        end_date__lte=timezone.now().date() + timedelta(days=30),
        is_active=True
    ).count()

    # Payments
    agent_payments = RentPayment.objects.filter(lease__agent=agent)
    total_revenue = agent_payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    this_month = timezone.now().replace(day=1, hour=0, minute=0, second=0)
    monthly_revenue = agent_payments.filter(payment_date__gte=this_month).aggregate(total=Sum('amount_paid'))['total'] or 0

    # Maintenance
    maintenance = MaintenanceRequest.objects.filter(property__agent=agent)
    pending_maintenance = maintenance.filter(status='pending').count()

    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'total_properties': total_properties,
        'available_properties': available_properties,
        'total_tenants': total_tenants,
        'new_tenants_this_month': new_tenants_this_month,
        'total_leases': total_leases,
        'active_leases': active_leases,
        'leases_ending_soon': leases_ending_soon,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'pending_maintenance': pending_maintenance,
        'recent_leases': agent_leases.order_by('-created_at')[:5],
        'recent_payments': agent_payments.order_by('-payment_date')[:5],
        'recent_maintenance': maintenance.order_by('-requested_on')[:5],
        'recent_properties': agent_properties.order_by('-created_at')[:6],
    }
    return render(request, 'frontend/agent_dashboard.html', context)


@login_required
def agent_properties_view(request):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    properties = Property.objects.filter(agent=agent).order_by('-created_at')
    
    # Search/filter
    search = request.GET.get('search')
    property_type = request.GET.get('type')
    status = request.GET.get('status')
    
    if search:
        properties = properties.filter(
            Q(property_name__icontains=search) | Q(location__icontains=search)
        )
    if property_type:
        properties = properties.filter(property_type=property_type)
    if status == 'available':
        properties = properties.filter(is_available=True)
    elif status == 'rented':
        properties = properties.filter(is_available=False)

    paginator = Paginator(properties, 10)
    page = request.GET.get('page')
    properties_page = paginator.get_page(page)

    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'properties': properties_page,
        'total_count': properties.count(),
        'available_count': properties.filter(is_available=True).count(),
        'property_types': Property._meta.get_field('property_type').choices,
    }
    return render(request, 'frontend/agent_properties.html', context)


@login_required
def agent_property_detail_view(request, pk):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    property_obj = get_object_or_404(Property, pk=pk, agent=agent)
    
    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'property': property_obj,
        'tenants': Tenant.objects.filter(agent=agent, property_name=property_obj.property_name),
        'leases': Lease.objects.filter(agent=agent, property=property_obj),
        'maintenance': MaintenanceRequest.objects.filter(property=property_obj),
    }
    return render(request, 'frontend/agent_property_detail.html', context)


@login_required
def agent_tenants_view(request):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    tenants = Tenant.objects.filter(agent=agent).order_by('-created_at')
    
    search = request.GET.get('search')
    if search:
        tenants = tenants.filter(
            Q(property_name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search)
        )

    paginator = Paginator(tenants, 10)
    page = request.GET.get('page')
    tenants_page = paginator.get_page(page)

    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'tenants': tenants_page,
        'total_count': tenants.count(),
        'active_count': tenants.filter(is_active=True).count(),
    }
    return render(request, 'frontend/agent_tenants.html', context)


@login_required
def agent_leases_view(request):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    leases = Lease.objects.filter(agent=agent).order_by('-created_at')
    
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        leases = leases.filter(is_active=True)
    elif status_filter == 'expired':
        leases = leases.filter(is_active=False)

    paginator = Paginator(leases, 10)
    page = request.GET.get('page')
    leases_page = paginator.get_page(page)

    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'leases': leases_page,
        'total_count': leases.count(),
        'active_count': leases.filter(is_active=True).count(),
        'ending_soon_count': leases.filter(
            end_date__lte=timezone.now().date() + timedelta(days=30),
            is_active=True
        ).count(),
    }
    return render(request, 'frontend/agent_leases.html', context)


@login_required
def agent_payments_view(request):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    payments = RentPayment.objects.filter(lease__agent=agent).order_by('-payment_date')
    
    # Summary
    total_revenue = payments.aggregate(total=Sum('amount_paid'))['total'] or 0
    this_month = timezone.now().replace(day=1, hour=0, minute=0, second=0)
    monthly_revenue = payments.filter(payment_date__gte=this_month).aggregate(total=Sum('amount_paid'))['total'] or 0

    paginator = Paginator(payments, 15)
    page = request.GET.get('page')
    payments_page = paginator.get_page(page)

    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'payments': payments_page,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'total_count': payments.count(),
    }
    return render(request, 'frontend/agent_payments.html', context)


@login_required
def agent_maintenance_view(request):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    maintenance = MaintenanceRequest.objects.filter(property__agent=agent).order_by('-requested_on')
    
    status_filter = request.GET.get('status')
    if status_filter:
        maintenance = maintenance.filter(status=status_filter)

    paginator = Paginator(maintenance, 10)
    page = request.GET.get('page')
    maintenance_page = paginator.get_page(page)

    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'maintenance': maintenance_page,
        'total_count': maintenance.count(),
        'pending_count': maintenance.filter(status='pending').count(),
        'in_progress_count': maintenance.filter(status='in_progress').count(),
        'resolved_count': maintenance.filter(status='resolved').count(),
    }
    return render(request, 'frontend/agent_maintenance.html', context)


@login_required
def agent_inspections_view(request):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    inspections = Inspection.objects.filter(property__agent=agent).order_by('-inspection_date')
    
    status_filter = request.GET.get('status')
    if status_filter:
        inspections = inspections.filter(status=status_filter)

    paginator = Paginator(inspections, 10)
    page = request.GET.get('page')
    inspections_page = paginator.get_page(page)

    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'inspections': inspections_page,
        'total_count': inspections.count(),
        'scheduled_count': inspections.filter(status='scheduled').count(),
        'completed_count': inspections.filter(status='completed').count(),
    }
    return render(request, 'frontend/agent_inspections.html', context)


@login_required
def agent_analytics_view(request):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    # Performance metrics
    properties = Property.objects.filter(agent=agent)
    tenants = Tenant.objects.filter(agent=agent)
    leases = Lease.objects.filter(agent=agent)
    payments = RentPayment.objects.filter(lease__agent=agent)

    # Monthly revenue for chart
    monthly_data = []
    for i in range(11, -1, -1):
        month_start = (timezone.now().replace(day=1) - timedelta(days=i*30)).replace(day=1)
        month_end = (month_start + timedelta(days=32)).replace(day=1)
        month_revenue = payments.filter(
            payment_date__gte=month_start,
            payment_date__lt=month_end
        ).aggregate(total=Sum('amount_paid'))['total'] or 0
        monthly_data.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': float(month_revenue)
        })

    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
        'total_properties': properties.count(),
        'total_tenants': tenants.count(),
        'total_leases': leases.count(),
        'total_revenue': payments.aggregate(total=Sum('amount_paid'))['total'] or 0,
        'occupancy_rate': round((leases.filter(is_active=True).count() / max(properties.count(), 1)) * 100, 1),
        'avg_rent': leases.aggregate(avg=Sum('rent_amount'))['avg'] or 0,
        'monthly_data': monthly_data,
        'properties_by_type': list(properties.values('property_type').annotate(count=Count('id'))),
    }
    return render(request, 'frontend/agent_analytics.html', context)


@login_required
def agent_settings_view(request):
    agent = get_agent_or_redirect(request)
    if not agent:
        return redirect('frontend:home')

    if request.method == 'POST':
        # Update agent profile
        agent.first_name = request.POST.get('first_name', agent.first_name)
        agent.last_name = request.POST.get('last_name', agent.last_name)
        agent.phone_number = request.POST.get('phone_number', agent.phone_number)
        agent.bio = request.POST.get('bio', agent.bio)
        agent.commission_rate = request.POST.get('commission_rate', agent.commission_rate)
        agent.agency_name = request.POST.get('agency_name', agent.agency_name)
        agent.business_reg_no = request.POST.get('business_reg_no', agent.business_reg_no)
        agent.license_no = request.POST.get('license_no', agent.license_no)
        agent.physical_address = request.POST.get('physical_address', agent.physical_address)
        agent.city = request.POST.get('city', agent.city)
        agent.country = request.POST.get('country', agent.country)
        
        if request.FILES.get('profile_picture'):
            agent.profile_picture = request.FILES['profile_picture']
        
        agent.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('frontend:agent_settings')

    context = {
        'agent': agent,
        'agent_name': f"{agent.first_name} {agent.last_name}",
    }
    return render(request, 'frontend/agent_settings.html', context)


# ==================== PUBLIC PAGES ====================

def home_view(request):
    featured_properties = Property.objects.filter(is_featured=True, is_available=True).order_by('-created_at')[:3]
    return render(request, 'frontend/home.html', {'featured_properties': featured_properties})


def about_view(request):
    testimonials = [
        {"name": "Sarah Jenkins", "role": "Administrative Director", "content": "Working with Zia Properties has completely streamlined our operations."},
        {"name": "Michael Chen", "role": "Operations Manager", "content": "A truly comprehensive platform. The maintenance tools are intuitive."}
    ]
    return render(request, 'frontend/about.html', {'testimonials': testimonials})


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
    location = request.GET.get('location')
    property_type = request.GET.get('type')

    if location:
        properties = properties.filter(location__icontains=location)
    if property_type:
        properties = properties.filter(property_type__iexact=property_type)

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


def testimonials_view(request):
    testimonials = Testimonial.objects.filter(is_visible=True).order_by('-created_at')
    return render(request, 'frontend/testimonials.html', {'testimonials': testimonials})


@login_required
def premium_agent_page(request):
    return render(request, 'frontend/premium_agent.html')


@login_required
def payment_success(request):
    return render(request, 'frontend/payment_success.html')


def payment_failed(request):
    return render(request, 'frontend/payment_failed.html')


def mpesa_waiting(request):
    checkout_id = request.GET.get("checkout_id")
    return render(request, "frontend/mpesa_waiting.html", {"checkout_id": checkout_id})