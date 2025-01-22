from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from addressBook.contacts.forms import ContactCreateForm, ContactBaseForm
from addressBook.contacts.models import Contact
from addressBook.labels.models import Label


# Contact list view that only shows contacts for the logged-in user
class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "address-book.html"
    context_object_name = "contacts"

    paginate_by = 10

    def get_queryset(self):
        queryset = Contact.objects.filter(user=self.request.user)

        search = self.request.GET.get("search", "").strip()
        if search:
            queryset = queryset.filter(first_name__icontains=search) | queryset.filter(last_name__icontains=search)

        category = self.request.GET.get("category", "").strip()
        if category and category != "all":
            queryset = queryset.filter(labels__name__iexact=category)

        sort = self.request.GET.get("sort", "a-z")
        if sort == "a-z":
            queryset = queryset.order_by("first_name", "last_name")
        elif sort == "z-a":
            queryset = queryset.order_by("-first_name", "-last_name")

        return queryset

    def get_context_data(self, **kwargs):
        # Add user-specific labels to the context for filtering contacts
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['user_labels'] = user.labels.all()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if AJAX
            contacts_html = render_to_string('contacts/container-contacts.html', context, request=self.request)
            paginator_html = render_to_string('common/paginator.html', context, request=self.request)
            return JsonResponse({
                'contacts_html': contacts_html,
                'paginator_html': paginator_html
            })
        return super().render_to_response(context, **response_kwargs)


# View for creating a new contact
class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactCreateForm
    template_name = "contacts/create-contact.html"
    success_url = reverse_lazy('address-book')

    def form_valid(self, form):
        # Associate the new contact with the logged-in user
        form.instance.user = self.request.user

        try:
            # Try saving the form, if successful, return valid response
            return super().form_valid(form)
        except IntegrityError:
            # If a contact with the same name already exists, add an error
            form.add_error(None, "A contact with this name already exists.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        # Pass all available labels to the context to be used in the form
        context = super().get_context_data(**kwargs)
        context['labels'] = Label.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs


# View for editing an existing contact
class ContactEditView(LoginRequiredMixin, UpdateView):
    model = Contact
    form_class = ContactBaseForm
    template_name = 'contacts/edit-contact.html'
    success_url = reverse_lazy('address-book')

    def dispatch(self, request, *args, **kwargs):
        # Ensure the user is trying to edit their own contact
        contact = get_object_or_404(Contact, pk=self.kwargs['pk'])

        # If the contact does not belong to the user, redirect them to the address book
        if contact.user != request.user:
            return HttpResponseRedirect(reverse('address-book'))

        # Proceed with the original dispatch if the user owns the contact
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    def form_valid(self, form):
        # Associate the updated contact with the logged-in user
        form.instance.user = self.request.user

        try:
            # Attempt to save the form and return a valid response
            return super().form_valid(form)
        except IntegrityError:
            # If contact with the same name exists, add an error
            form.add_error(None, "A contact with this name already exists.")
            return self.form_invalid(form)


# View for deleting a contact
class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'contacts/delete-contact.html'
    success_url = reverse_lazy('address-book')

    def dispatch(self, request, *args, **kwargs):
        # Ensure the user is deleting their own contact
        contact = get_object_or_404(Contact, pk=self.kwargs['pk'])

        # If the contact does not belong to the user, redirect them to the home page
        if contact.user != request.user:
            return HttpResponseRedirect(reverse('home'))

        # Proceed with the original dispatch if the user owns the contact
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Retrieve the specific contact to be deleted
        return get_object_or_404(Contact, pk=self.kwargs['pk'])


# View for displaying details of a specific contact
class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'contacts/contact-details.html'
    context_object_name = 'contact'

    def dispatch(self, request, *args, **kwargs):
        # Ensure the user is trying to view their own contact
        contact = get_object_or_404(Contact, pk=self.kwargs['pk'])

        # If the contact does not belong to the user, redirect them to the address book
        if contact.user != request.user:
            return HttpResponseRedirect(reverse('address-book'))

        # Proceed with the original dispatch if the user owns the contact
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Retrieve the specific contact based on the pk in the URL
        return get_object_or_404(Contact, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # Return the context data as is (no additional data needed for now)
        context = super().get_context_data(**kwargs)
        return context
