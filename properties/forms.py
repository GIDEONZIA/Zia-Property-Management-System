
from django import forms
from .models import BuyerLead, SellerLead

class BuyerLeadForm(forms.ModelForm):
    class Meta:
        model = BuyerLead
        fields = ['name', 'email', 'phone', 'preferred_location', 'budget', 'message']

class SellerLeadForm(forms.ModelForm):
    class Meta:
        model = SellerLead
        fields = ['name', 'email', 'phone', 'property_location', 'asking_price', 'message']
