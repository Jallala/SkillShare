# SkillShare/skillswap_review/urls.py
from django.urls import path
from . import views


app_name = 'skillswap_review'

urlpatterns = [
    path('review/<str:username>/<int:skill_id>/', views.submit_review, name='submit_review'),
    # path("review/submit/", views.submit_review, name="submit_review"),
    # path('review/<int:user_id>/', views.submit_review, name='submit_review'),

]