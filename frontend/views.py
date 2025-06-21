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
