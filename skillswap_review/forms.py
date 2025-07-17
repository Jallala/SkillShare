
# SkillShare/skillswap_review/forms.py
from django import forms
from skillswap_common.models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['review', 'rating']  
        widgets = {
            'review': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
