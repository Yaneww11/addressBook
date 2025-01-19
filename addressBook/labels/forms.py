from django import forms
from .models import Label


# Base form class for creating or editing a label
class LabelBaseForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'color']
        # Define the widgets for the form fields to specify their behavior and appearance
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


# Form for creating a new label, inherits from LabelBaseForm
class LabelCreateForm(LabelBaseForm):
    # No additional changes or functionality are needed, just inherits from the base form
    pass


# Form for editing an existing label, inherits from LabelBaseForm
class LabelEditForm(LabelBaseForm):
    # Like LabelCreateForm, inherits all behavior from the base form
    pass
