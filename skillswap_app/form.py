from django import forms
from .models import Skill

class SkillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Select'
        self.fields['type'].choices = [('', 'Select')] + list(self.fields['type'].choices)[1:]

    class Meta:
        model = Skill
        fields = ['title', 'category', 'description', 'availability', 'location', 'type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
