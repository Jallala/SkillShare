from django.shortcuts import render
from skillswap_common.models import Skill

def skill_list(request):
    skills = Skill.objects.all()
    return render(request, 'search/skill_list.html', {'skills': skills})

