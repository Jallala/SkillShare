# SkillShare/skillswap_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .form import SkillForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from skillswap_common.models import Skill, Category
from skillswap_app import form
from django.contrib.auth.models import User
from django.views.generic import DetailView
from skillswap_common.models import Skill, Rating
from django.views.generic import DetailView
from django.db.models import Avg

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
    skills = []
    categories = Category.objects.all()

    if query:
        skills = Skill.objects.filter(title__icontains=query)
    else:
        skills = Skill.objects.all()

    return render(request, 'search.html', {
        'skills': skills,
        'categories': categories,
        'query': query
    })



class SkillDetailView(DetailView):
    model = Skill
    template_name = 'skill_detail.html'
    context_object_name = 'skill'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill = self.get_object()

        # Reviews only for this skill
        context['ratings'] = Rating.objects.filter(skill=skill)

        context['all_reviews_for_user'] = Rating.objects.filter(reviewee=skill.user).exclude(skill=skill)

        context['average_rating'] = Rating.objects.filter(skill=skill).aggregate(avg=Avg('rating'))['avg']

        return context




from django.contrib.auth.models import User
# from users.models import UserProfile # Adjust 'users' to your app name if different

print("Checking existing users and creating profiles if missing...")

# Get all users
all_users = User.objects.all()

if not all_users.exists():
    print("No users found in the database.")
else:
    for user in all_users:
        try:
            # Try to get the user's profile
            profile = user.userprofile
            print(f"User '{user.username}' (ID: {user.id}) already has a profile (ID: {profile.id}).")
            # Optional: You can update existing profiles here if needed
            # For example:
            if not profile.bio:
                profile.bio = f"Default bio for {user.username}"
                profile.save()
                print(f"  - Updated bio for {user.username}")

        except UserProfile.DoesNotExist:
            # If a profile does not exist, create one
            print(f"User '{user.username}' (ID: {user.id}) does NOT have a profile. Creating one now...")
            new_profile = UserProfile.objects.create(user=user)
            print(f"  - Profile created for '{user.username}' with ID: {new_profile.id}.")
            # You can set default values for the new profile here
            new_profile.bio = "Default bio."
            new_profile.location = "Unknown"
            new_profile.save()

        except Exception as e:
            print(f"An unexpected error occurred for user '{user.username}': {e}")

print("\nProfile creation/check process complete.")
