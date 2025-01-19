from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, TemplateView, UpdateView
from django.http import HttpResponseRedirect

from addressBook.users.forms import UserRegisterForm, UserLoginForm, CustomPasswordResetForm, UserProfileEditForm
from addressBook.users.models import AppUser, Profile

UserModel = get_user_model()


# View for user registration
class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    # Redirect authenticated users to the home page
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save the user and log them in
        user = form.save()
        user.backend = 'addressBook.users.backends.EmailOrUsernameBackend'
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy('home'))


# View for user login
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True  # Redirect authenticated users to the default redirect URL


# View to confirm and process user logout
class LogoutConfirmView(TemplateView):
    template_name = 'accounts/logout.html'

    # Handle POST requests for logout
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


# View for password change
class CustomPasswordResetView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change-password.html'
    form_class = CustomPasswordResetForm

    # Redirect to the user's profile page upon successful password change
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    # Fetch the current user object
    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(AppUser, username=username)

    # Update the user's password and save
    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['new_password1'])
        user.save()
        return super().form_valid(form)


# View to display user profile
class UserProfileView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    # Fetch the currently logged-in user
    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        # Add additional data to the context
        context['contact_count'] = user.contacts.count()
        return context


# View to edit user profile
class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "accounts/edit-profile.html"
    form_class = UserProfileEditForm

    # Fetch the profile of the currently logged-in user
    def get_object(self, queryset=None):
        return self.request.user.profile

    # Populate initial form data with user and profile information
    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'username': self.request.user.username,
            'email': self.request.user.email,
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
        })
        return initial

    # Redirect to the profile page upon successful update
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    # Save updated user and profile information
    def form_valid(self, form):
        profile = form.save(commit=False)

        # Update user attributes
        user = self.request.user
        user.username = form.cleaned_data.get('username', user.username)
        user.email = form.cleaned_data.get('email', user.email)
        user.first_name = form.cleaned_data.get('first_name', user.first_name)
        user.last_name = form.cleaned_data.get('last_name', user.last_name)
        user.save()

        # Save the updated profile
        profile.save()

        return super().form_valid(form)
