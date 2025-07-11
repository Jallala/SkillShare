from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from typing import TYPE_CHECKING
from skillswap_common.models import UserProfile, Message
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.db.models import QuerySet


def contact_user(request: 'HttpRequest', uid: int, text: str) -> HttpResponse:
    try:
        user = request.user
        send_request_to = UserProfile.objects.get(pk=uid)
        message = Message(sender=user, receiver=send_request_to, text=text)
        message.save()
        send_request_to.messages.add(message)
    except ValueError:
        # TODO Check text length, and that both users exist
        logger.exception('Error sending message')
        return JsonResponse({'success': False})
    return JsonResponse({'success': True})


def get_inbox(request: 'HttpRequest') -> HttpResponse:
    user = request.user
    messages: 'QuerySet[Message]' = Message.objects.filter(
        Q(receiver=user.id) | Q(sender=user.id))
    return JsonResponse([m.as_dict() for m in messages])
