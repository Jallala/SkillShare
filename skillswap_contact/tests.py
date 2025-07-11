from django.test import TestCase
from django.contrib.auth.models import User
from skillswap_common import models
# Create your tests here.

class ContactTestCase(TestCase):
    counter = 1
    users: 'list[tuple[User, models.UserProfile]]' = []

    def _create_user_with_profile(self):
        auth = (f'test{self.counter}', f'test{self.counter}@test.com', 'password')
        user = User.objects.create_user(*auth)
        user.save()
        user_profile = models.UserProfile(user=user)
        user_profile.save()
        self.users.append((user, user_profile))
        self.counter += 1
        return 

    def setUp(self):
        self._create_user_with_profile()
        self._create_user_with_profile()
        return super().setUp()
    
    def test_can_send_message(self):
        _, sender = self.users[0]
        _, receiver = self.users[1]
        message = sender.send_message(receiver, 'Hello')
        print(message)
        assert message in sender.messages()
        assert message in receiver.messages()
        