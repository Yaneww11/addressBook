from django.urls import path
from addressBook.labels.views import LabelListView, LabelCreateView, LabelEditView, LabelDeleteView

urlpatterns = [
    path('list/', LabelListView.as_view(), name='labels-list'),
    path('create/', LabelCreateView.as_view(), name='create-label'),
    path('edit/<int:pk>/', LabelEditView.as_view(), name='edit-label'),
    path('delete/<int:pk>/', LabelDeleteView.as_view(), name='delete-label'),
]