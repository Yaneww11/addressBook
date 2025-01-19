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


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user.backend = 'addressBook.users.backends.EmailOrUsernameBackend'
        login(self.request, user)

        return HttpResponseRedirect(reverse_lazy('home'))


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class LogoutConfirmView(TemplateView):
    template_name = 'accounts/logout.html'

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class CustomPasswordResetView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/change-password.html'
    form_class = CustomPasswordResetForm

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(AppUser, username=username)

    def form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['new_password1'])
        user.save()
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['contact_count'] = user.contacts.count()
        return context


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = "accounts/edit-profile.html"
    form_class = UserProfileEditForm

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'username': self.request.user.username,
            'email': self.request.user.email,
            'first_name': self.request.user.first_name,
            'last_name': self.request.user.last_name,
        })
        return initial

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        profile = form.save(commit=False)

        user = self.request.user
        user.username = form.cleaned_data.get('username', user.username)
        user.email = form.cleaned_data.get('email', user.email)
        user.first_name = form.cleaned_data.get('first_name', user.first_name)
        user.last_name = form.cleaned_data.get('last_name', user.last_name)
        user.save()

        profile.save()

        return super().form_valid(form)

class UserProfileDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/delete-profile.html'

    def post(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.email = f'{user.email}_deleted'
        user.username = f'{user.username}_deleted'
        user.save()
        logout(request)
        return redirect('home')