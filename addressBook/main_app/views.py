from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
def home_view(request):
    return render(request, 'index.html')


def address_book_view(request):
    return render(request, 'address-book.html')