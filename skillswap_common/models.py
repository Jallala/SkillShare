from django.db import models

# Create your models here.
from . import abc


class Skill(models.Model):
    name = models.CharField(max_length=256, blank=False)


class Rating(models.Model):
    name = models.CharField(max_length=256, blank=False)
    rated_at = models.DateTimeField('Rated At', auto_created=True)
    rated_by = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)


class Message(models.Model):
    message = models.TextField(max_length=4096)
    sent_at = models.DateTimeField('Sent at', auto_now_add=True)
    sender = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='+')
    reciever = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, related_name='+')


class UserProfile(models.Model):
    skills = models.ManyToManyField(Skill)
    ratings = models.ManyToManyField(Rating)
    messages = models.ManyToManyField(Message)
