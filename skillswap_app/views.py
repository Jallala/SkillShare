
from django.shortcuts import render, redirect, get_object_or_404
from .form import SkillForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from skillswap_common.models import Skill, Category
from skillswap_app import form
from django.contrib.auth.models import User


def create_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            try:
                skill = form.save(commit=False)
                skill.user = request.user
                skill.save()
                messages.success(request, 'Skill saved successfully!')
                return redirect('create_skill')  # Or wherever you want
            except:
                messages.error(
                    request, 'Form submission failed. Please save again.')
                return redirect('create_skill')  # Or wherever you want
    else:
        form = SkillForm()

    return render(request, 'skills.html', {'form': form, 'is_edit': False})


@login_required
def update_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Skill updated successfully!')
                return redirect('update_skill',skill_id=skill.id)  # Replace with your skill list view name
            except Exception as e:
                messages.error(request, f'Error updating skill: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SkillForm(instance=skill)

    return render(request, 'skills.html', {'form': form, 'is_edit': True})

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)

    if request.method == 'POST':
        print(f"Deleting skill: {skill.id}")  # Debug
        skill.delete()
        messages.success(request, 'Skill deleted successfully!')
        return redirect('profile')  # <-- make sure 'profile' is your profile URL name

    return redirect('profile')

def search_skills_view(request):
    query = request.GET.get('q', '').strip()
    users = []
    skills = []
    categories = Category.objects.all() 

    if query:
        users = User.objects.filter(username__icontains=query)
        skills = Skill.objects.filter(title__icontains=query)
    else:
        skills = Skill.objects.all()  

    return render(request, 'search.html', {
        'users': users,
        'skills': skills,
        'categories': categories,
        'query': query
    })
