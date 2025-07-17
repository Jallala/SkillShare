import logging
from typing import TYPE_CHECKING

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


if TYPE_CHECKING:
    from typing import Literal
    KEYS = Literal['message', 'sent_at', 'sender', 'receiver']
    from django.db.models import QuerySet

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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills_needed = models.CharField(max_length=255, blank=True)
    skills_offered = models.CharField(max_length=255, blank=True)
    skills = models.ManyToManyField(Skill)
    ratings = models.ManyToManyField(Rating)

    @classmethod
    def get_user_profile_from(cls, uid_or_user: 'int | User | UserProfile') -> 'UserProfile':
        if isinstance(uid_or_user, cls):
            return uid_or_user
        elif isinstance(uid_or_user, int):
            try:
                user = User.objects.get(pk=uid_or_user)
            except User.DoesNotExist as ex:
                raise UserProfile.DoesNotExist('User does not exist') from ex
            profile, _ = UserProfile.objects.get_or_create(user=user)
            return profile

        assert uid_or_user in User.objects
        return UserProfile.objects.get(user=uid_or_user)

    def for_template(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
        }


class Message(models.Model):
    sender = models.ForeignKey(
        'Messages', on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(
        'Messages', on_delete=models.CASCADE, related_name='+')
    message = models.TextField(max_length=4096)
    sent_at = models.DateTimeField('Sent at', auto_now_add=True)

    def as_dict(self) -> 'dict[KEYS, str]':
        return {
            'message': self.message,
            'sent_at': self.sent_at.isoformat(),
            'sender': self.sender.id,
            'receiver': self.receiver.id
        }

    def for_template(self) -> 'dict[KEYS, str | dict[str, str]]':
        sender: 'Messages' = self.sender
        receiver: 'Messages' = self.receiver
        return {
            'message': self.message,
            'sent_at': self.sent_at.isoformat(),
            'sender': sender.for_template(),
            'receiver': receiver.for_template()
        }

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.message}'

class Messages(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message)

    def send_message(self, other: 'Messages | int | User | UserProfile', text: str) -> 'Message':
        other: 'Messages' = Messages.get_messages_for(other)
        if other is not None:
            message = Message(sender=self, receiver=other, message=text)
            message.save()
            self.messages.add(message)
            other.messages.add(message)
            return message
        assert False

    def get_messages(self) -> 'QuerySet[Message]':
        return self.messages.order_by('sent_at')
    
    def get_chat_log_with(self, uid: int) -> 'QuerySet[Message]':
        other = User.objects.get(pk=uid)
        other_messages, _ = Messages.objects.get_or_create(user=other)
        return self.messages.filter(Q(receiver=other_messages) | Q(sender=other_messages)).order_by('sent_at')

    @classmethod
    def get_messages_for(cls, uid_or_user: 'Messages | int | User | UserProfile') -> 'Messages | None':
        messages = None
        user = None
        if isinstance(uid_or_user, cls):
            return uid_or_user
        elif isinstance(uid_or_user, int):
            try:
                user = User.objects.get(pk=uid_or_user)
            except User.DoesNotExist as ex:
                raise Messages.DoesNotExist('User does not exist') from ex
            return Messages.objects.get(user=user)

        if isinstance(uid_or_user, UserProfile):
            user = uid_or_user.user
        elif isinstance(uid_or_user, User):
            user = uid_or_user
        if not user:
            logger.warning('Could not convert {} into {}',
                           uid_or_user, cls.__name__)
            raise Messages.DoesNotExist('User does not exist')

        messages, _ = Messages.objects.get_or_create(user=user)
        return messages

    def for_template(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
        }

    def __str__(self):
        return f'Messages for {self.user.username}'