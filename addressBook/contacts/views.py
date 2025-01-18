from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from addressBook.contacts.forms import ContactCreateForm, ContactBaseForm
from addressBook.contacts.models import Contact
from addressBook.labels.models import Label


# Create your views here.
class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "address-book.html"
    context_object_name = "contacts"
    paginate_by = 2

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_labels'] = Label.objects.all()
        return context


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactCreateForm
    template_name = "contacts/create-contact.html"
    success_url = reverse_lazy('address-book')

    def form_valid(self, form):
        form.instance.user = self.request.user

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "A contact with this name already exists.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all()
        return context


class ContactEditView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactBaseForm
    template_name = 'contacts/edit-contact.html'
    success_url = reverse_lazy('address-book')

    def dispatch(self, request, *args, **kwargs):
        contact = get_object_or_404(Contact, pk=self.kwargs['pk'])

        if contact.user != request.user:
            return HttpResponseRedirect(reverse('address-book'))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        print(f"Uploaded file: {self.request.FILES.get('image')}")
        form.instance.user = self.request.user

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "A contact with this name already exists.")
            return self.form_invalid(form)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'contacts/delete-contact.html'
    success_url = reverse_lazy('address-book')

    def dispatch(self, request, *args, **kwargs):
        contact = get_object_or_404(Contact, pk=self.kwargs['pk'])

        if contact.user != request.user:
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Contact, pk=self.kwargs['pk'])


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contacts/contact-details.html'
    context_object_name = 'contact'

    def get_object(self, queryset=None):
        return get_object_or_404(Contact, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context