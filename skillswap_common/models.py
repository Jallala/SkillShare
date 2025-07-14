import logging
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
# Create your models here.
from . import abc

if TYPE_CHECKING:
    from django.db.models import QuerySet

logger = logging.getLogger(__name__)


class SkillCategory(models.Model):
    name = models.CharField(max_length=256)


class Skill(models.Model):
    OFFER = 'O'
    REQUEST = 'R'
    TYPE = {
        OFFER: 'Offer',
        REQUEST: 'Request'
    }
    user = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='+')
    title = models.CharField(max_length=256, blank=False)
    description = models.TextField(max_length=4096)
    availability = models.BooleanField(default=True)
    location = models.CharField(max_length=256)
    skill_type = models.CharField(max_length=1, choices=TYPE, default=OFFER)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE)


class Rating(models.Model):
    name = models.CharField(max_length=256, blank=False)
    rated_at = models.DateTimeField('Rated At', auto_now_add=True)
    rated_by = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills_needed = models.CharField(max_length=255, blank=True)
    skills_offered = models.CharField(max_length=255, blank=True)
    skills = models.ManyToManyField(Skill)
    ratings = models.ManyToManyField(Rating)
    @classmethod
    def convert_to_user_profile(cls, uid_or_user: 'int | User | UserProfile') -> 'UserProfile | None':
        if isinstance(uid_or_user, (int, User)):
            return UserProfile.objects.get(user=uid_or_user)
        elif isinstance(uid_or_user, cls):
            return uid_or_user
        logger.warning('Could not convert {} into UserProfile',
                       (uid_or_user, ))
        return None

    def for_template(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
        }
