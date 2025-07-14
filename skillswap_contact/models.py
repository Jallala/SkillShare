from django.db import models

from django.db.models import Q
from django.contrib.auth.models import User

import logging
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from django.db.models import QuerySet

logger = logging.getLogger(__name__)


class Message(models.Model):
    sender = models.ForeignKey(
        'Messages', on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(
        'Messages', on_delete=models.CASCADE, related_name='+')
    message = models.TextField(max_length=4096)
    sent_at = models.DateTimeField('Sent at', auto_now_add=True)

    def as_dict(self):
        return {
            'message': self.message,
            'sent_at': self.sent_at.isoformat(),
            'sender': self.sender.id,
            'receiver': self.receiver.id
        }

    def for_template(self):
        sender: 'Messages' = self.sender
        receiver: 'Messages' = self.receiver
        return {
            'message': self.message,
            'sent_at': self.sent_at.isoformat(),
            'sender': sender.for_template(),
            'receiver': receiver.for_template()
        }


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message)

    def send_message(self, other: 'Messages | int | User', message: str):
        other = Messages.convert_to_messages(other)
        if other is not None:
            message = Message(sender=self, receiver=other, message=message)
            message.save()
            return message
        assert False

    def get_messages(self) -> 'QuerySet[Message]':
        return Message.objects.filter(Q(receiver=self) | Q(sender=self)).order_by('sent_at')

    @classmethod
    def convert_to_messages(cls, uid_or_user: 'int | User | Messages') -> 'Messages | None':
        if isinstance(uid_or_user, (int, User)):
            return Messages.objects.get(user=uid_or_user)
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
