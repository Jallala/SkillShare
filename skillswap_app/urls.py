from django.urls import path
from skillswap_app import views


urlpatterns = [
    path('skills', views.create_skill, name='create_skill'),
    path('search/', views.search_skills_view, name='search'),
]
