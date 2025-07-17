# SkillShare/skillswap_review/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages # For user feedback messages
from skillswap_common.models import Skill,Rating # Assuming Skill model is here
from .models import Review # Your Review model
from django.contrib.auth.models import User
from .forms import RatingForm


@login_required
def submit_review(request, username, skill_id):
    print("ubmit_review view triggered")

    reviewee = get_object_or_404(User, username=username)
    skill = get_object_or_404(Skill, id=skill_id)

    if request.user.is_authenticated and request.user != reviewee:
        rating_instance, created = Rating.objects.get_or_create(
            reviewer=request.user,
            reviewee=reviewee,
            skill=skill
        )

        if request.method == 'POST':
            form = RatingForm(request.POST, instance=rating_instance)

            if form.is_valid():
                rating = form.save(commit=False)
                rating.reviewer = request.user
                rating.reviewee = reviewee
                rating.skill = skill
                rating.save()
                if created:
                    messages.success(request, "Your review has been submitted successfully!")
                else:
                    messages.success(request, "Your review has been updated successfully!")
            else:
                messages.error(request, "Please correct the errors in the form.")
        else:
            form = RatingForm(instance=rating_instance)

        # return redirect('user_profile', username=reviewee.username)
        return redirect('skill_detail', pk=skill.id)


    else:
        messages.error(request, "You cannot review this user.")
        return redirect('skill_detail', pk=skill.id)

