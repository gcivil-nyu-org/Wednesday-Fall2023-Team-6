from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.messages import get_messages, constants

from MediLink.settings import MESSAGE_TAGS


class LoginTests(TestCase):

    def setUp(self):
        self.user_email = "test_user@gmail.com"
        self.user_password = "test_password"
        User.objects.create_user(self.user_email, self.user_email, self.user_password)

    def test_01_existing_user(self):
        print("\nRunning: test for checking login of existing user")
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")
        
        post_data = {"user_email": self.user_email, "user_pwd": self.user_password}
        response = self.client.post("/user/login/", post_data)
        logged_in_user = auth.get_user(self.client)
        self.assertEqual(logged_in_user.get_username(), self.user_email)
        self.assertTrue(logged_in_user.is_authenticated)
        self.assertRedirects(
            response=response,
            expected_url="/user/home/",
            status_code=302,
            target_status_code=200,
        )

        print("Completed: test for checking login of existing user")

    def test_02_nonexisting_user(self):
        print("\nRunning: test for checking login of nonexisting user")
        post_data = {"user_email": "invalid_email", "user_pwd": "invalid_password"}
        response = self.client.post("/user/login/", post_data)
        logged_in_user = auth.get_user(self.client)
        self.assertFalse(logged_in_user.is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.ERROR])
        self.assertNotEqual(logged_in_user.get_username(), "invalid_email")

        self.assertRedirects(
            response=response,
            expected_url="/user/login/",
            status_code=302,
            target_status_code=200,
        )
        print("Completed: test for checking login of nonexisting user\n")

    def tearDown(self):
        self.client.logout()
