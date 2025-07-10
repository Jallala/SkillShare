from django.urls import path
from skillswap_app import views


urlpatterns = [
    path('skills', views.index, name='index'), 
]
