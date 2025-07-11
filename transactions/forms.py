from django import forms
from .models import MpesaTransaction
from properties.models import Tenant, Lease

class RentPaymentForm(forms.Form):
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    lease = forms.ModelChoiceField(
        queryset=Lease.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    payment_method = forms.ChoiceField(
        choices=[('mpesa', 'M-Pesa'), ('cash', 'Cash'), ('bank', 'Bank Transfer')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    reference_number = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    receipt = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
