from django.urls import path

from addressBook.users.views import UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
]