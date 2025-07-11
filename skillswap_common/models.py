import logging
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

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


class Message(models.Model):
    sender = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='+')
    message = models.TextField(max_length=4096)
    sent_at = models.DateTimeField('Sent at', auto_now_add=True)

    def as_dict(self):
        return {
            'message': self.message,
            'sent_at': self.sent_at.isoformat(),
            'sender': self.sender.id,
            'reciever': self.reciever.id
        }

    @classmethod
    def send(cls, sender: 'UserProfile | User', receiver: 'UserProfile | User', message: str):
        cls(sender, receiver, message)


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill)
    ratings = models.ManyToManyField(Rating)
    messages = models.ManyToManyField(Message)

    def send_message(self, other: 'UserProfile | int | User', message: str):
        other = UserProfile.convert_to_user_profile(other)
        if other is not None:
            message = Message(sender=self, receiver=other, message=message)
            message.save()
            return message
        assert False

    def inbox(self) -> 'QuerySet[Message]':
        return Message.objects.filter(Q(receiver=self) | Q(sender=self)).order_by('sent_at')

    @classmethod
    def convert_to_user_profile(cls, uid_or_user: 'int | User | UserProfile') -> 'UserProfile | None':
        if isinstance(uid_or_user, (int, User)):
            return UserProfile.objects.get(user=uid_or_user)
        elif isinstance(uid_or_user, cls):
            return uid_or_user
        logger.warning('Could not convert {} into UserProfile',
                       (uid_or_user, ))
        return None
        self.assertContains
