from django.shortcuts import render
from django.views.generic import TemplateView


def home_view(request):
    return render(request, 'index.html')

def address_book_view(request):
    return render(request, 'address-book.html')