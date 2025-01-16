from django.urls import path
from django.contrib.auth.views import LogoutView
from addressBook.users.views import UserLoginView, UserRegisterView, UserProfileView, LogoutConfirmView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutConfirmView.as_view(), name='logout'),
]
