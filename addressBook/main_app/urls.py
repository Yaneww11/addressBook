from django.urls import path, include

from addressBook.main_app.views import home_view, address_book_view

urlpatterns = [
    path('', home_view, name='home'),
    path('addres-book/', address_book_view, name='address-book'),
]