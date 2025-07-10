from django.shortcuts import render, redirect
from .form import SkillForm
from django.contrib.auth.decorators import login_required

#@login_required
def sample_file(request):
    return render(request,'sample.html')


def create_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        print(request)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            print(request.user)
            skill.save()

            return redirect('sample_file')  # Or wherever you want
    else:
        form = SkillForm()
    return render(request, 'index.html', {'form': form})


