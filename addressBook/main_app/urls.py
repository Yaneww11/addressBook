from django.urls import path, include
from addressBook.main_app.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('addres-book/', include('addressBook.contacts.urls')),
]