from django.urls import path
from skillswap_contact import views

API_USER_MESSAGES = 'skillswap_contact.api.messages'
API_USER_CONTACT = 'skillswap_contact.api.contact'
USER_MESSAGES = 'skillswap_contact.messages'
urlpatterns = [
    path('messages/', views.api_messages, name=API_USER_MESSAGES),
    path('view_messages/', views.messages, name=USER_MESSAGES),
    path('user/<int:uid>/', views.contact_user, name=API_USER_CONTACT),
]
