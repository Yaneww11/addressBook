from django import forms
from django.core.exceptions import ValidationError

from .models import Contact
from ..labels.models import Label


class ContactBaseForm(forms.ModelForm):
    class Meta:
        model = Contact

        fields = [
            'first_name', 'last_name', 'image', 'phone_number',
            'company_name', 'address', 'company_phone', 'email',
            'fax_number', 'comment', 'labels'
        ]

        required = [
            'first_name', 'phone_number'
        ]

        # Define custom widgets for each field to style and provide placeholder text
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

    def clean_labels(self):
        labels = self.cleaned_data.get('labels')

        if labels.count() > 5:
            raise ValidationError("A contact can have a maximum of 5 labels.")

        return labels

    def __init__(self, *args, **kwargs):
        # Extract the user from the kwargs
        self.user = kwargs.pop('user', None)  # Pop the user from the kwargs
        super().__init__(*args, **kwargs)

        if self.user:
            # Filter the 'labels' queryset to only show labels for the current user
            self.fields['labels'].queryset = Label.objects.filter(user=self.user)


# ContactCreateForm inherits ContactBaseForm and can be customized further if needed
class ContactCreateForm(ContactBaseForm):
    pass


