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
    properties = Property.objects.all()
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
                recipient_list=['gwiternz@gmail.com'],  # 🔁 Change to your receiving email
                fail_silently=False,
            )
            messages.success(request, "Message sent successfully.")
            return redirect('contact')  # reloads the page with success msg
        except Exception as e:
            messages.error(request, f"Failed to send message: {e}")
            return redirect('contact')

    return render(request, 'frontend/contact.html')



def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, 'frontend/blog.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    return render(request, 'frontend/blog_detail.html', {'post': post})
            