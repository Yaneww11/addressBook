from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.forms import TextInput, EmailInput
from django.core.exceptions import ValidationError

from addressBook.users.models import Profile


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'placeholder': "Enter Password"
            }
        )

        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'placeholder': "Confirm Password"
            }
        )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {
            'username': TextInput(
                attrs={
                    'placeholder': 'Enter your username',
                }
            ),
            'email': EmailInput(
                attrs={
                    'placeholder': 'Enter your email',
                }
            ),
            'first_name': TextInput(
                attrs={
                    'placeholder': 'Enter your first name',
                }
            ),
            'last_name': TextInput(
                attrs={
                    'placeholder': 'Enter your last name',
                }
            )
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username or email',
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
        })
    )

    labels = [

    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email_or_username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Use the custom backend
        self.user_cache = authenticate(self.request, username=email_or_username, password=password)
        if self.user_cache is None:
            raise forms.ValidationError("Please enter a correct username/email and password.")
        else:
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class CustomPasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password'
            }
        ),
        label='New Password'
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm new password'
            }
        ),
        label='Confirm New Password'
    )


class UserProfileEditForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )

    class Meta:
        model = Profile
        fields = ['profile_picture', 'phone_number']
        widgets = {
            'profile_picture': forms.ClearableFileInput(),
            'phone_number': forms.TextInput(
                attrs={'placeholder': 'Enter your phone number', 'required': False}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reorder fields here
        self.fields = {
            'username': self.fields['username'],
            'email': self.fields['email'],
            'first_name': self.fields['first_name'],
            'last_name': self.fields['last_name'],
            'phone_number': self.fields['phone_number'],
            'profile_picture': self.fields['profile_picture'],
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_model = get_user_model()
        if user_model.objects.filter(username=username).exclude(id=self.instance.user.id).exists():
            raise ValidationError("This username is already taken.")
        return username
