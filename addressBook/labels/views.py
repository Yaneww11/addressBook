from django.shortcuts import render, get_object_or_404

from addressBook.labels.forms import LabelCreateForm, LabelEditForm
from addressBook.labels.models import Label
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect


# Create your views here.
class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels/labels.html"
    context_object_name = "labels"

    def get_queryset(self):
        return Label.objects.filter(user=self.request.user)


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelCreateForm
    template_name = "labels/create-label.html"
    success_url = reverse_lazy('labels-list')

    def form_valid(self, form):
        form.instance.user = self.request.user

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "A label with this name already exists.")
            return self.form_invalid(form)


class LabelEditView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelEditForm
    template_name = 'labels/edit-label.html'
    success_url = reverse_lazy('labels-list')

    def dispatch(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=self.kwargs['pk'])

        if label.user != request.user:
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user

        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "A label with this name already exists.")
            return self.form_invalid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete-label.html'
    success_url = reverse_lazy('labels-list')

    def dispatch(self, request, *args, **kwargs):
        label = get_object_or_404(Label, pk=self.kwargs['pk'])

        if label.user != request.user:
            return HttpResponseRedirect(reverse('home'))

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(Label, pk=self.kwargs['pk'])
