from django.urls import path
from django.contrib.auth.views import LogoutView
from addressBook.users.views import UserLoginView, UserRegisterView, UserProfileView, LogoutConfirmView, \
    CustomPasswordResetView, UserProfileEditView, UserProfileDeleteView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutConfirmView.as_view(), name='logout'),
    path('change-password/', CustomPasswordResetView.as_view(), name='change-password'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
    path('edit/', UserProfileEditView.as_view(), name='edit-profile'),
    path('delete/', UserProfileDeleteView.as_view(), name='delete-profile'),
]
