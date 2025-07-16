from django.shortcuts import render
from django.contrib.auth.models import User
from skillswap_common.models import Skill

def skill_list(request):
    query = request.GET.get('q', '').strip()
    users = []
    skills = []

    if query:
        users = User.objects.filter(username__icontains=query)
        skills = Skill.objects.filter(title__icontains=query)

    return render(request, 'search/skill_list.html', {
        'users': users,
        'skills': skills,
        'query': query
    })