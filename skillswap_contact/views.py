import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from typing import TYPE_CHECKING
from .models import Messages, Message

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.db.models import QuerySet

TEMPLATE_MESSAGES_PAGE = 'skillswap/messages.html'

@login_required
def contact_user(request: 'HttpRequest', uid: int) -> HttpResponse:
    try:
        user = request.user
        if request.method == 'POST':
            message = request.POST['message']
            messages = Messages.objects.get(user=user)
            send_request_to = Messages.objects.get(pk=uid)
            messages.send_message(send_request_to, message=message)
    except (KeyError, ValueError):
        # TODO Check text length, and that both users exist
        logger.exception('Error sending message')
        return JsonResponse({'success': False})
    return JsonResponse({'success': True})


def _get_messages(request: 'HttpRequest') -> 'QuerySet[Message]':
    user = request.user
    messages: 'QuerySet[Message]' = Message.objects.filter(
        Q(receiver=user.id) | Q(sender=user.id))
    return messages


@login_required
def api_messages(request: 'HttpRequest') -> HttpResponse:
    messages = _get_messages(request)
    return JsonResponse({'messages': [m.as_dict() for m in messages]})


@login_required
def messages(request: 'HttpRequest') -> HttpResponse:
    messages = _get_messages(request)
    return render(request, TEMPLATE_MESSAGES_PAGE, context={'messages': [m.for_template() for m in messages]})
