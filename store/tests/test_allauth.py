from django.test import TestCase
from django.contrib import auth
from django.urls import reverse

from store import models


class TestSignUp(TestCase):
    def setUp(self):
        self.post_user_data = {
            "username": "username543",
            "email": "user@domain.com",
            "password1": "abcabcabc",
            "password2": "abcabcabc",
        }

    def test_user_signup_page_loads_correctly(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')


    def test_user_signup_page_submission_works(self):
        post_data = self.post_user_data
        response = self.client.post(
            reverse("account_signup"), post_data
        )

        # Redirect to home
        self.assertEqual(response.status_code, 302)

        # Is it logged in?
        self.assertTrue(
            auth.get_user(self.client).is_authenticated
        )

    def test_user_login_page_loads_correctly(self):
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
