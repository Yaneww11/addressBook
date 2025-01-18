from django import forms
from .models import Contact


class ContactBaseForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'phone_number',
            'company_name', 'address', 'company_phone', 'email',
            'fax_number', 'comment', 'labels', 'image'
        ]
        required = [
            'first_name', 'phone_number'
        ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Enter first name'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Enter last name'}
            ),
            'phone_number': forms.TextInput(
                attrs={'placeholder': 'Enter phone number'}
            ),
            'company_name': forms.TextInput(
                attrs={'placeholder': 'Enter company name'}
            ),
            'address': forms.Textarea(
                attrs={'placeholder': 'Enter address'}
            ),
            'company_phone': forms.TextInput(
                attrs={'placeholder': 'Enter company phone'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Enter email'}
            ),
            'fax_number': forms.TextInput(
                attrs={'placeholder': 'Enter fax number'}
            ),
            'comment': forms.Textarea(
                attrs={'placeholder': 'Enter comment'}
            ),
            'labels': forms.SelectMultiple(),
            'image': forms.ClearableFileInput()
        }


class ContactCreateForm(ContactBaseForm):
    pass