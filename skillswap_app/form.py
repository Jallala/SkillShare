from django import forms
from .models import Skill

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['title', 'category', 'description', 'availability', 'location', 'type']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'type': forms.Select(),
        }
