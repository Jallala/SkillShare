from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import ProfileForm, UserForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from skillswap_common.models import Skill,Rating
from skillswap_common.models import UserProfile
from django.db.models import Avg


from django.conf import settings
print(settings.TEMPLATES[0]['DIRS'])


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(
                request, 'Account created successfully!'
            )
            return redirect('edit_profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def profile_view(request):
    profile = UserProfile.objects.get(user=request.user)
    skills_offered = Skill.objects.filter(user=profile.user, type='offer')
    skills_needed = Skill.objects.filter(user=profile.user, type='request')


     # Get all reviews for skills offered by the user
    skill_ids = skills_offered.values_list('id', flat=True)
    all_reviews = Rating.objects.filter(skill_id__in=skill_ids).select_related('reviewer')

    # Calculate overall rating from all received reviews
    overall_rating = all_reviews.aggregate(Avg('rating'))['rating__avg']


    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'user_is_owner': True,
        'skills_offered': skills_offered,
        'skills_needed': skills_needed,

        'overall_rating': overall_rating, 
        'all_reviews': all_reviews,
    })






@login_required
def edit_profile(request):
    user: 'User' = request.user
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
