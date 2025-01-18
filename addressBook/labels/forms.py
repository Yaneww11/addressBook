from django import forms
from .models import Label


class LabelBaseForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'color']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter label name'
                }
            ),
            'color': forms.TextInput(
                attrs={
                    'type': 'color',
                    'placeholder': 'Choose label color'
                }
            ),
        }


class LabelCreateForm(LabelBaseForm):
    pass


class LabelEditForm(LabelBaseForm):
    pass

