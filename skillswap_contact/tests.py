from django.test import TestCase, Client
from unittest import skip
from django.contrib.auth.models import User
from django.urls import reverse
from skillswap_common import models
from . import urls
# Create your tests here.


class ContactTestCase(TestCase):
    counter = 1
    users: 'list[tuple[User, models.UserProfile]]' = []
    message_to_1 = None
    message_to_2 = None
    sender = None
    receiver = None
    receiver2 = None
    other = None
    auth = {}

    def _create_user_with_profile(self):
        auth = {
            'username': f'test{self.counter}',
            'email': f'test{self.counter}@test.com',
            'password': 'password'
        }
        user = User.objects.create_user(**auth)
        self.auth[user.id] = auth
        user.save()
        user_profile = models.UserProfile.objects.create(user=user)
        user_profile.save()
        self.users.append((user, user_profile))
        self.counter += 1
        return user_profile

    def setUp(self):
        _ignored_user_to_offset_ids = User.objects.create_user(username='ignored', email='ignore@test.se', password='password')

        self.sender = models.Messages.get_messages_for(self._create_user_with_profile())
        self.receiver = models.Messages.get_messages_for(self._create_user_with_profile())
        self.receiver2 = models.Messages.get_messages_for(self._create_user_with_profile())
        self.other = models.Messages.get_messages_for(self._create_user_with_profile())

        self.message_to_1 = self.sender.send_message(self.receiver, 'Hello, nr1')
        self.message_to_2 = self.sender.send_message(self.receiver2, 'Hello, nr2')
        self.reply_1 = self.receiver.send_message(self.sender, 'Hello, sender from 1')
        self.reply_2 = self.receiver2.send_message(self.sender, 'Hello, sender from 2')
        return super().setUp()

    def test_both_have_the_message(self):
        self.assertIn(self.message_to_1, self.sender.get_messages())
        self.assertIn(self.message_to_2, self.sender.get_messages())
        self.assertIn(self.message_to_1, self.receiver.get_messages())
        self.assertIn(self.message_to_2, self.receiver2.get_messages())

    def test_other_users_cannot_see_messages_from(self):
        self.assertEqual(len(self.other.get_messages()), 0)
        self.assertNotIn(self.message_to_1, self.other.get_messages())
        self.assertNotIn(self.message_to_1, self.receiver2.get_messages())

    def test_get_chat_with_specific_id(self):
        chat = self.sender.get_chat_log_with(self.receiver2.user.id)
        for message in chat:
            if message.sender == self.receiver2:
                self.assertTrue(message.receiver == self.sender)
            else:
                self.assertTrue(message.receiver == self.receiver2 and message.sender == self.sender)

    def test_send_fails_if_user_does_not_exist(self):
        non_exisiting_user_id = max(self.auth.keys()) + 1
        with self.assertRaises(models.Messages.DoesNotExist):
            self.sender.send_message(non_exisiting_user_id, 'Hello')

    # TODO Depends if contacting should be a REST API or not
    def test_api_get_inbox(self):
        client = Client()
        client.login(**self.auth[self.sender.user.id])
        request = client.get(reverse(urls.API_USER_MESSAGES))
        data = request.json()
        self.assertIn('messages', data)
        self.assertEqual(data['messages'][0]['sender'], self.sender.id)
        self.assertEqual(data['messages'][0]['receiver'], self.receiver.id)
    

    # TODO Depends if contacting should be a REST API or not
    @skip('Not ready yet')
    def test_api_get_unauthorized(self):
        client = Client()
        request = client.get(reverse(urls.API_USER_MESSAGES))

    def test_send_message(self):
        client = Client()
        client.login(**self.auth[self.sender.user.id])
        endpoint = reverse(urls.API_USER_CONTACT, kwargs={'uid': self.receiver.user.id})
        message_text = 'Hello, Requesting Skill'
        request = client.post(endpoint, data={'message': message_text})
        self.assertTrue(request.json()['success'])
        last_message = list(self.receiver.get_messages())[-1]
        self.assertEqual(list(self.sender.get_messages())[-1], last_message)
        self.assertEqual(message_text, last_message.message)
        self.assertEqual(self.sender.id, last_message.sender.id)
        self.assertEqual(self.receiver.id, last_message.receiver.id)
    
