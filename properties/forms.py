from django import forms
from .models import BuyerLead, SellerLead, Property, Tenant, Lease, RentPayment, MaintenanceRequest, Inspection


class BuyerLeadForm(forms.ModelForm):
    class Meta:
        model = BuyerLead
        fields = ['name', 'email', 'phone', 'preferred_location', 'budget', 'message']


class SellerLeadForm(forms.ModelForm):
    class Meta:
        model = SellerLead
        fields = ['name', 'email', 'phone', 'property_location', 'asking_price', 'message']


class AgentPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['is_featured', 'available']  # Fixed typo: 'availabele' → 'available'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # So we can pass request.user when initializing
        super().__init__(*args, **kwargs)
        if user and not user.is_superuser:
            if 'agent' in self.fields:
                self.fields['agent'].disabled = True

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ['agent']


class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        exclude = ['agent']  # agent is auto-assigned based on the logged-in user
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'signed_date': forms.DateInput(attrs={'type': 'date'}),
            'renewal_date': forms.DateInput(attrs={'type': 'date'}),
            'termination_date': forms.DateInput(attrs={'type': 'date'}),
            'rent_payment_date': forms.DateInput(attrs={'type': 'date'}),
            'termination_fee_paid_date': forms.DateInput(attrs={'type': 'date'}),
            'renewal_fee_paid_date': forms.DateInput(attrs={'type': 'date'}),
        }



class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['property', 'issue', 'status']


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['property', 'inspection_date', 'inspector_name', 'notes', 'status']
class RentPaymentForm(forms.ModelForm):
    class Meta:
        model = RentPayment
        fields = '__all__'  # or specify needed fields
