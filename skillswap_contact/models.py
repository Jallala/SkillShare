from django.db import models

from django.db.models import Q
from django.contrib.auth.models import User

import logging
from typing import TYPE_CHECKING

from django.db import models
from skillswap_common.models import UserProfile


if TYPE_CHECKING:
    from typing import Literal
    KEYS = Literal['message', 'sent_at', 'sender', 'receiver']
    from django.db.models import QuerySet

logger = logging.getLogger(__name__)


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


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message)

    def send_message(self, other: 'Messages | int | User | UserProfile', text: str) -> 'Message':
        other = Messages.get_messages_from(other)
        if other is not None:
            message = Message(sender=self, receiver=other, message=text)
            message.save()
            self.messages.add(message)
            other.messages.add(message)
            return message
        assert False

    def get_messages(self) -> 'QuerySet[Message]':
        return Message.objects.filter(Q(receiver=self) | Q(sender=self)).order_by('sent_at')

    @classmethod
    def get_messages_from(cls, uid_or_user: 'Messages | int | User | UserProfile') -> 'Messages | None':
        messages = None
        user = None
        if isinstance(uid_or_user, cls):
            return uid_or_user
        elif isinstance(uid_or_user, int):
            try:
                user = User.objects.get(pk=uid_or_user)
            except User.DoesNotExist:
                raise Messages.DoesNotExist('User does not exist')
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
