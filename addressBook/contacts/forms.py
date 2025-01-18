from django import forms
from .models import Contact

class ContactBaseForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'image', 'company_name',
            'address','company_phone', 'email', 'fax_number',
            'phone_number', 'comment', 'labels'
        ]
        required = [
            'first_name', 'phone_number'
        ]
        widgets = {
            'image': forms.ClearableFileInput()
        }

class ContactCreateForm(ContactBaseForm):
    pass