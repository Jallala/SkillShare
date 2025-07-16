import logging

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from typing import TYPE_CHECKING
from skillswap_common.models import UserProfile, Message, Messages

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from django.http import HttpRequest
    from django.db.models import QuerySet

TEMPLATE_CHAT_PAGE = 'skillswap/chat.html'
TEMPLATE_MESSAGES_PAGE = 'skillswap/messages.html'

def _send_message(user: 'User', to_uid: int, message: str):
    messages = Messages.get_messages_for(user)
    messages.send_message(to_uid, text=message)


@login_required
def contact_user(request: 'HttpRequest', uid: int) -> HttpResponse:
    try:
        user = request.user
        if request.method == 'POST':
            message = request.POST['message']
            _send_message(user, to_uid=uid, message=message)
    except (KeyError, ValueError, UserProfile.DoesNotExist):
        # TODO Check text length, and that both users exist
        logger.exception('Error sending message')
        return JsonResponse({'success': False})
    return JsonResponse({'success': True})


def _get_messages(request: 'HttpRequest') -> 'QuerySet[Message]':
    user = request.user
    messages = Messages.get_messages_for(user)
    return messages.messages.get_queryset()


@login_required
def api_messages(request: 'HttpRequest') -> HttpResponse:
    messages = _get_messages(request)
    return JsonResponse({'messages': [m.as_dict() for m in messages]})


@login_required
def messages(request: 'HttpRequest') -> HttpResponse:
    messages = _get_messages(request)
    chats = {}
    for message in messages.order_by('-sent_at'):
        to_other: 'Messages' = message.receiver if message.receiver is not messages else message.sender
        if to_other.id not in chats:
            chats[to_other.id] = {
                'chat_with': to_other.user.username,
                'last_message': message.for_template()
            }
    return render(request, TEMPLATE_MESSAGES_PAGE, context={'chats': chats, 'chat_base_url': 'skillswap_contact.chat'})


@login_required
def chat_with_user(request: 'HttpRequest', uid: int) -> HttpResponse:
    all_messages = Messages.get_messages_for(request.user)
    other_user = UserProfile.objects.get(user=uid)
    messages_with_user = all_messages.get_chat_log_with(uid)
    if request.method == 'POST':
        try:
            contact_user(request, uid)
        except (KeyError, ValueError, UserProfile.DoesNotExist):
            raise
    context = {
        'chat': [m.for_template() for m in messages_with_user],
        'other': other_user.for_template()
    }
    return render(request, TEMPLATE_CHAT_PAGE, context=context)
