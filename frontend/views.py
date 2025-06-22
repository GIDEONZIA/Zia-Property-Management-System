from django.shortcuts import render, redirect
from .forms import CustomSignupForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomSignupForm()
    
    return render(request, 'frontend/sign_up.html', {'form': form})




from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'frontend/login.html'
    authentication_form = AuthenticationForm



from django.shortcuts import render
from properties.models import Property  # import from your app

def idx_search_view(request):
    properties = Property.objects.filter(is_available=True)

    location = request.GET.get('location')
    property_type = request.GET.get('type')
    price = request.GET.get('price')

    if location:
        properties = properties.filter(location__icontains=location)
    if property_type:
        properties = properties.filter(property_type__iexact=property_type)
    if price:
        try:
            price = float(price)
            properties = properties.filter(price__lte=price)
        except ValueError:
            pass

    return render(request, 'frontend/idx_search.html', {'properties': properties})

                 