from django.shortcuts import render, redirect
from .form import SkillForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from skillswap_common.models import Skill, Category

# @login_required


def create_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        print(request)
        if form.is_valid():
            try:
                skill = form.save(commit=False)
                skill.user = request.user
                print(request.user)
                skill.save()
                messages.success(request, 'Skill saved successfully!')
                return redirect('create_skill')  # Or wherever you want
            except:
                messages.error(
                    request, 'Form submission failed. Please save again.')
                return redirect('create_skill')  # Or wherever you want
    else:
        form = SkillForm()
    return render(request, 'skills.html', {'form': form})


def search_skills_view(request):
    categories = Category.objects.all()
    skills = Skill.objects.all()
    return render(request, 'search.html', {
        'categories': categories,
        'skills': skills,
    })
