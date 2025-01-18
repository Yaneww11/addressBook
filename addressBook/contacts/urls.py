from django.urls import include
from django.urls import path
from addressBook.contacts.views import ContactListView, ContactCreateView, ContactEditView, ContactDetailView, \
    ContactDeleteView

urlpatterns = [
    path('', ContactListView.as_view(), name='address-book'),
    path('create/', ContactCreateView.as_view(), name='create-contact'),
    path('<int:pk>/', include([
        path('edit/', ContactEditView.as_view(), name='edit-contact'),
        path('', ContactDetailView.as_view(), name='detail-contact'),
        path('delete/', ContactDeleteView.as_view(), name='delete-contact'),
    ])),

]