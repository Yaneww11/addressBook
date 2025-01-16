from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView, TemplateView
from django.http import HttpResponseRedirect

from addressBook.users.forms import UserRegisterForm, UserLoginForm
from addressBook.users.models import AppUser

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


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(AppUser, username=username)

