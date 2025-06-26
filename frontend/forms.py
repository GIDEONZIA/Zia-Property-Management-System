from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class CustomSignupForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)

        # ✅ Add custom CSS classes to each input field
        self.fields['username'].widget.attrs.update({'class': 'signup-input'})
        self.fields['email'].widget.attrs.update({'class': 'signup-input'})
        self.fields['password1'].widget.attrs.update({'class': 'signup-input'})
        self.fields['password2'].widget.attrs.update({'class': 'signup-input'})
        self.fields['phone'].widget.attrs.update({'class': 'signup-input'})


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'signup-input',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'signup-input',
            'placeholder': 'Enter your password'
        })

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Contact Message from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            ['gwiternz@gmail.com'],  # Or your receiving email
            fail_silently=False
        )

        messages.success(request, "Message sent successfully.")
        return redirect('contact')  # Or wherever you want to go

    return render(request, 'frontend/contact.html')
