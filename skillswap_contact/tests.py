from django.test import TestCase, Client
from unittest import skip
from django.contrib.auth.models import User
from django.urls import reverse
from . import models, urls
# Create your tests here.


class ContactTestCase(TestCase):
    counter = 1
    users: 'list[tuple[User, models.UserProfile]]' = []
    message = None
    sender = None
    receiver = None
    other = None
    auth = {}

    def _create_user_with_profile(self):
        auth = {
            'username': f'test{self.counter}',
            'email': f'test{self.counter}@test.com',
            'password': 'password'
        }
        self.auth[self.counter] = auth
        user = User.objects.create_user(**auth)
        user.save()
        user_profile = models.UserProfile.objects.create(user=user)
        user_profile.save()
        self.users.append((user, user_profile))
        self.counter += 1
        return user_profile

    def setUp(self):
        self.sender = models.Messages.get_messages_for(self._create_user_with_profile())
        self.receiver = models.Messages.get_messages_for(self._create_user_with_profile())
        self.other = models.Messages.get_messages_for(self._create_user_with_profile())

        self.message = self.sender.send_message(self.receiver, 'Hello')
        return super().setUp()

    def test_both_have_the_message(self):
        self.assertIn(self.message, self.sender.get_messages())
        self.assertIn(self.message, self.receiver.get_messages())

    def test_other_users_cannot_see_messages_from(self):
        self.assertEqual(len(self.other.get_messages()), 0)
        self.assertNotIn(self.message, self.other.get_messages())

    def test_send_fails_if_user_does_not_exist(self):
        non_exisiting_user_id = self.counter
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
    
    def test_api_get_inbox(self):
        client = Client()
        client.login(**self.auth[self.sender.user.id])
        request = client.get(reverse(urls.USER_MESSAGES))
        print(request.content)

    # TODO Depends if contacting should be a REST API or not
    @skip('Not ready yet')
    def test_api_get_unauthorized(self):
        client = Client()
        request = client.get(reverse(urls.API_USER_MESSAGES))

    def test_send_message(self):
        client = Client()
        client.login(**self.auth[self.sender.user.id])
        endpoint = reverse(urls.API_USER_CONTACT, kwargs={'uid': self.receiver.id})
        message_text = 'Hello, Requesting Skill'
        request = client.post(endpoint, data={'message': message_text})
        self.assertTrue(request.json()['success'])
        last_message = list(self.receiver.get_messages())[-1]
        self.assertEqual(list(self.sender.get_messages())[-1], last_message)
        self.assertEqual(message_text, last_message.message)
        self.assertEqual(self.sender.user.id, last_message.sender.id)
        self.assertEqual(self.receiver.user.id, last_message.receiver.id)
    
