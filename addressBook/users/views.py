from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

UserModel = get_user_model()
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

class UserRegistrationView(CreateView):
    model = UserModel
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

