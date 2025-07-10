from django.db import models

# Create your models here.
from . import abc
from django.utils.dates import 

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
    skills = models.ManyToManyField(Skill)
    ratings = models.ManyToManyField(Rating)
    messages = models.ManyToManyField(Message)
