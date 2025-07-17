# SkillShare/skillswap_review/models.py

from django.db import models
from django.contrib.auth.models import User # For the user who writes the review
from skillswap_common.models import Skill # Import the Skill model from skillswap_common

class Review(models.Model):
    # The user who is writing the review
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')

    # The skill that is being reviewed
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='reviews')

    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, help_text="Rating from 1 to 5 stars")

    # The "comment" of the review
    comment = models.TextField(blank=True, null=True, help_text="Optional review comment")

    # # Timestamps
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures a user can only submit one review for a specific skill
        unique_together = ('user', 'skill')
        # # Order reviews by most recent first by default
        # ordering = ['-created_at']

