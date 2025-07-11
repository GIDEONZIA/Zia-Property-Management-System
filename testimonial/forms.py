from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'role', 'message', 'photo']  # No 'is_visible' since it's admin only

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Tenant, Landlord, Buyer'}),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your feedback here...',
                'rows': 5
            }),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
