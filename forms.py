from django import forms
from .models import Donor

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            'full_name',
            'age',
            'gender',
            'blood_group',
            'phone',
            'email',
            'city',
            'address',
            'last_donation_date',
            'availability'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name (e.g. Rajesh Kumar)',
                'required': True
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age (18 - 65)',
                'min': '18',
                'max': '65',
                'required': True
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'blood_group': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10-digit mobile number',
                'pattern': r'^\+?[0-9]{10,15}$',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
                'required': True
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City (e.g. Chennai)',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Street address, area, pincode',
                'required': True
            }),
            'last_donation_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'availability': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 18 or age > 65):
            raise forms.ValidationError("Eligible donor age must be between 18 and 65 years.")
        return age

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        import re
        if not re.match(r'^\+?[0-9]{10,15}$', phone):
            raise forms.ValidationError("Please provide a valid 10-15 digit phone number.")
        return phone
