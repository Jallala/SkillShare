from django.contrib import admin
from skillswap_app.models import Skill,Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Skill)