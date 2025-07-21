
# skillswap_review/views.py
from django.shortcuts import redirect, get_object_or_404
from skillswap_common.models import Skill, Rating
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# # Create your views here.
# @login_required
# def submit_review(request, username, skill_id):
#     print("ubmit_review view triggered")

#     reviewee = get_object_or_404(User, username=username)
#     skill = get_object_or_404(Skill, id=skill_id)

#     if request.user.is_authenticated and request.user != reviewee:
#         rating_instance, created = Rating.objects.get_or_create(
#             reviewer=request.user,
#             reviewee=reviewee,
#             skill=skill
#         )

#         if request.method == 'POST':
#             form = RatingForm(request.POST, instance=rating_instance)

#             if form.is_valid():
#                 rating = form.save(commit=False)
#                 rating.reviewer = request.user
#                 rating.reviewee = reviewee
#                 rating.skill = skill
#                 rating.save()
#                 if created:
#                     messages.success(request, "Your review has been submitted successfully!")
#                 else:
#                     messages.success(request, "Your review has been updated successfully!")
#             else:
#                 messages.error(request, "Please correct the errors in the form.")
#         else:
#             form = RatingForm(instance=rating_instance)

#         return return redirect('skill_detail', pk=skill_id)
#     else:
#         messages.error(request, "You cannot review this user.")
#         return redirect('skill_detail', pk=skill_id)



@login_required
def submit_review(request, username, skill_id):
    if request.method == 'POST':
        skill = get_object_or_404(Skill, id=skill_id)
        reviewee = get_object_or_404(User, username=username)
        rating_value = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '')

        # Either update or create a new review
        rating_obj, created = Rating.objects.update_or_create(
            reviewer=request.user,
            reviewee=reviewee,
            skill=skill,
            defaults={'rating': rating_value, 'review': comment}
        )

        messages.success(request, "Your review has been submitted.")
        return redirect('skill_detail', pk=skill_id)





# from django.db import models

# # Create your models here.
# @login_required
# def submit_review_view(request): # Removed user_id from arguments
#     if request.method == 'POST':
#         skill_id = request.POST.get('skill_id')
#         rating = request.POST.get('rating') # Get as string, convert later
#         comment = request.POST.get('comment')

#         # Basic validation
#         if not skill_id or not rating or not comment:
#             messages.error(request, "All fields (skill, rating, comment) are required.")
#             return redirect(request.META.get('HTTP_REFERER', 'profile')) # Redirect back to the previous page or default profile

#         try:
#             rating = int(rating) # Convert rating to integer
#             if not (1 <= rating <= 5):
#                 raise ValueError("Rating must be between 1 and 5.")
#         except ValueError:
#             messages.error(request, "Invalid rating value.")
#             return redirect(request.META.get('HTTP_REFERER', 'profile'))

#         try:
#             skill = get_object_or_404(Skill, id=skill_id)
#         except ValueError: # Catch if skill_id isn't a valid integer string
#             messages.error(request, "Invalid skill ID provided.")
#             return redirect(request.META.get('HTTP_REFERER', 'profile'))

#         # The user whose skill is being reviewed (the skill owner)
#         reviewed_user_instance = skill.owner # Assuming skill.owner is a User instance

#         # Prevent a user from reviewing their own skill/profile
#         if request.user == reviewed_user_instance:
#             messages.error(request, "You cannot review your own skill.")
#             return redirect(request.META.get('HTTP_REFERER', 'profile'))

#         # Create the review
#         Rating.objects.create(
#             reviewer=request.user,         # The logged-in user submitting the review
#             reviewed_user=reviewed_user_instance, # The User instance who owns the skill
#             skill=skill,                   # The specific skill being reviewed
#             rating=rating,
#             comment=comment
#         )
#         messages.success(request, "Your review has been submitted successfully!")
        
#         # Redirect back to the profile page of the user who owns the skill
#         # Assuming you have a URL pattern like path('profile/<int:user_id>/', views.profile_detail, name='profile_detail')
#         return redirect('profile_detail', user_id=reviewed_user_instance.id) # Replace 'profile_detail' with your actual URL name

#     return redirect('profile') # Fallback if method is not POST
