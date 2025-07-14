from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from . import views, urls
from . models import Profile
# Create your tests here.


class AccountsTestCase(TestCase):
    def test_create_account(self):
        client = Client()
        password = 'testpassword1'
        username = 'test_user'
        post_data = {
            'username': username,
            'email': 'test@test.com',
            'password1': password,
            'password2': password
        }

        resp = client.post(reverse(urls.SIGNUP), data=post_data)
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        self.assertTrue(user, 'User should exist')
        self.assertTrue(profile, 'User should have a profile')
        self.assertEqual(user.username, username)

    def setUp(self):
        pass
