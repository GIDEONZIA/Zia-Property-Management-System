from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import FileExtensionValidator

from properties.models import Agent, Property, Tenant, Lease, MaintenanceRequest, Inspection


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


# ==================== AGENT SIGNUP FORM ====================

class AgentSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="About Yourself / Bio")
    commission_rate = forms.DecimalField(max_digits=5, decimal_places=2, required=False, initial=5.00, label="Commission Rate (%)")
    agency_name = forms.CharField(max_length=200, required=False, label="Agency Name (if any)")
    business_reg_no = forms.CharField(max_length=100, required=False, label="Business Registration Number")
    license_no = forms.CharField(max_length=100, required=False, label="Real Estate License Number")
    physical_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False, label="Physical Address")
    city = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, initial="Kenya", required=False)
    agent_type = forms.ChoiceField(choices=Agent.AGENT_TYPE_CHOICES, initial='independent', required=True, label="Agent Classification")
    years_of_experience = forms.IntegerField(min_value=0, initial=0, required=False)
    properties_managed = forms.IntegerField(min_value=0, initial=0, required=False)
    profile_picture = forms.ImageField(required=False)
    id_document = forms.FileField(required=False, label="National ID / Passport (for verification)", validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])])
    business_certificate = forms.FileField(required=False, label="Business Certificate (optional)", validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'signup-input'})
            else:
                field.widget.attrs['class'] += ' signup-input'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            Agent.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email'],
                bio=self.cleaned_data.get('bio', ''),
                commission_rate=self.cleaned_data.get('commission_rate'),
                agency_name=self.cleaned_data.get('agency_name', ''),
                business_reg_no=self.cleaned_data.get('business_reg_no', ''),
                license_no=self.cleaned_data.get('license_no', ''),
                physical_address=self.cleaned_data.get('physical_address', ''),
                city=self.cleaned_data.get('city', ''),
                country=self.cleaned_data.get('country', 'Kenya'),
                agent_type=self.cleaned_data.get('agent_type', 'independent'),
                years_of_experience=self.cleaned_data.get('years_of_experience', 0),
                properties_managed=self.cleaned_data.get('properties_managed', 0),
                profile_picture=self.cleaned_data.get('profile_picture'),
                id_document=self.cleaned_data.get('id_document'),
                business_certificate=self.cleaned_data.get('business_certificate'),
                is_active=True,
            )
        return user


# ==================== PROPERTY CREATION FORM ====================

class PropertyCreateForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_name', 'address', 'description', 'property_type', 'location', 'price', 'currency', 'bedrooms', 'bathrooms', 'size', 'image', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'signup-input'})


# ==================== TENANT CREATION FORM ====================

class TenantCreateForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['property_name', 'email', 'phone', 'address', 'profile_picture']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'signup-input'})


# ==================== LEASE CREATION FORM ====================

class LeaseCreateForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['tenant', 'property', 'start_date', 'end_date', 'rent_amount', 'currency', 'lease_terms', 'security_deposit', 'payment_frequency', 'payment_method']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'lease_terms': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.agent = kwargs.pop('agent', None)
        super().__init__(*args, **kwargs)
        if self.agent:
            self.fields['tenant'].queryset = Tenant.objects.filter(agent=self.agent)
            self.fields['property'].queryset = Property.objects.filter(agent=self.agent)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'signup-input'})


# ==================== MAINTENANCE REQUEST FORM ====================

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['property', 'issue']
        widgets = {
            'issue': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.agent = kwargs.pop('agent', None)
        super().__init__(*args, **kwargs)
        if self.agent:
            self.fields['property'].queryset = Property.objects.filter(agent=self.agent)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'signup-input'})


# ==================== INSPECTION SCHEDULE FORM ====================

class InspectionScheduleForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = ['property', 'inspection_date', 'inspector_name', 'notes']
        widgets = {
            'inspection_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.agent = kwargs.pop('agent', None)
        super().__init__(*args, **kwargs)
        if self.agent:
            self.fields['property'].queryset = Property.objects.filter(agent=self.agent)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'signup-input'})