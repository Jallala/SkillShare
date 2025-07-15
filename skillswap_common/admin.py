from django.contrib import admin
from accounts.models import Profile
from .models import Category,Skill,Rating,Message,UserProfile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(Rating)
admin.site.register(Message)
admin.site.register(UserProfile)
