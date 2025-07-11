from django.urls import path
from skillswap_contact import views

USER_CONTACT = 'skillswap_contact.contact'
USER_INBOX = 'skillswap_contact.inbox'
urlpatterns = [
    path('inbox/', views.get_inbox, name=USER_INBOX),
    path('user/<int:id>/', views.contact_user, name=USER_CONTACT),
]
