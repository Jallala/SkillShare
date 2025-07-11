from django.test import TestCase
from django.contrib.auth.models import User
from skillswap_common import models
# Create your tests here.


class ContactTestCase(TestCase):
    counter = 1
    users: 'list[tuple[User, models.UserProfile]]' = []
    message = None
    sender = None
    receiver = None
    other = None

    def _create_user_with_profile(self):
        auth = (f'test{self.counter}',
                f'test{self.counter}@test.com', 'password')
        user = User.objects.create_user(*auth)
        user.save()
        user_profile = models.UserProfile(user=user)
        user_profile.save()
        self.users.append((user, user_profile))
        self.counter += 1
        return user_profile

    def setUp(self):
        self.sender = self._create_user_with_profile()
        self.receiver = self._create_user_with_profile()
        self.other = self._create_user_with_profile()

        self.message = self.sender.send_message(self.receiver, 'Hello')
        return super().setUp()

    def test_both_have_the_message(self):
        self.assertIn(self.message, self.sender.inbox())
        self.assertIn(self.message, self.receiver.inbox())

    def test_other_users_cannot_see_messages_from(self):
        self.assertEqual(len(self.other.inbox()), 0)
        self.assertNotIn(self.message, self.other.inbox())

    def test_send_fails_if_user_does_not_exist(self):
        non_exisiting_user_id = self.counter
        with self.assertRaises(models.UserProfile.DoesNotExist):
            self.sender.send_message(non_exisiting_user_id, 'Hello')
