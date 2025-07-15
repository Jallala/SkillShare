from django.db import models
from django.contrib.auth.models import User
from . import abc
import logging
logger = logging.getLogger(__name__)


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Skill(models.Model):
    TYPE_CHOICES = [
        ('offer', 'Offer'),
        ('request', 'Request'),
    ]

    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    availability = models.BooleanField()
    location = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.description} ({self.get_type_display()})"


class Rating(models.Model):
    name = models.CharField(max_length=256, blank=False)
    rated_at = models.DateTimeField('Rated At', auto_now_add=True)
    rated_by = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)


class Message(models.Model):
    message = models.TextField(max_length=4096)
    sent_at = models.DateTimeField('Sent at', auto_now_add=True)
    sender = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='+')
    reciever = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='+')

    def as_dict(self):
        return {
            'message': self.message,
            'sent_at': self.sent_at.isoformat(),
            'sender': self.sender.id,
            'reciever': self.reciever.id
        }


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

        logger = logging.getLogger(__name__)
        logger.warning('Could not convert {} into UserProfile',
                       (uid_or_user, ))
        return None

    def for_template(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
        }
