from django.urls import path
from skillswap_contact import views


urlpatterns = [
    path('contact_user', views.contact_user, name='Contact User'), 
    path('inbox', views.contact_user, name='Contact User'), 
]
