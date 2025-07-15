from django.contrib import admin

from .models import Category,Skill,Rating,Message,UserProfile

# Register your models here.
admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(Rating)
admin.site.register(Message)
admin.site.register(UserProfile)
