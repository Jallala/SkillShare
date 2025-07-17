from django.urls import path
from skillswap_app import views

urlpatterns = [
    #path('skills', views.create_skill, name='create_skill'),
    path('skills', views.create_skill, name='create_skill'),
    path('skills/<int:skill_id>/edit/', views.update_skill, name='update_skill'),
    path('skills/<int:skill_id>/delete/', views.delete_skill, name='delete_skill'),
    path('', views.search_skills_view, name='search'),
    path('skills/<int:pk>/', views.SkillDetailView.as_view(), name='skill_detail'),
]

