from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from typing import TYPE_CHECKING
from skillswap_common.models import UserProfile, Message
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.db.models import QuerySet

@login_required
def contact_user(request: 'HttpRequest', uid: int) -> HttpResponse:
    try:
        user = request.user
        if request.method == 'POST':
            text = request.POST['message']
            user_profile = UserProfile.objects.get(user=user)
            send_request_to = UserProfile.objects.get(pk=uid)
            message = Message(sender=user_profile,
                              receiver=send_request_to, text=text)
            message.save()
            send_request_to.inbox.add(message)
    except (KeyError, ValueError):
        # TODO Check text length, and that both users exist
        logger.exception('Error sending message')
        return JsonResponse({'success': False})
    return JsonResponse({'success': True})


@login_required
def get_inbox(request: 'HttpRequest') -> HttpResponse:
    user = request.user
    messages: 'QuerySet[Message]' = Message.objects.filter(
        Q(receiver=user.id) | Q(sender=user.id))
    return JsonResponse({'messages': [m.as_dict() for m in messages]})
