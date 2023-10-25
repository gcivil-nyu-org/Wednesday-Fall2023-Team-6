from django.core import mail
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages, constants
from MediLink.settings import MESSAGE_TAGS
from user.views import PASSWORD_RESET_SUBJECT


class ResetPasswordTests(TestCase):
    @classmethod
    def setUp(self):
        self.user_email = "test_user@gmail.com"
        self.user_password = "test_password"
        User.objects.create_user(self.user_email, self.user_email, self.user_password)

    def test_01_existing_user(self):
        print("\nRunning: test for checking password reset of existing user")
        response = self.client.get("/user/passwordReset/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/resetPassword/password_reset.html")

        response = self.client.post(
            "/user/passwordReset/", {"user_email": self.user_email}
        )
        self.assertRedirects(
            response=response,
            expected_url="/user/login/",
            status_code=302,
            target_status_code=200,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.SUCCESS])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, PASSWORD_RESET_SUBJECT)
        msgs = str(mail.outbox[0].message()).splitlines()
        for msg in msgs:
            if msg.startswith("http://"):
                uid = msg.split("/")[-2]
                token = msg.split("/")[-1]

        response = self.client.get(f"/user/passwordResetConfirm/{uid}/{token}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "user/resetPassword/password_reset_confirm.html"
        )

        response = self.client.post(
            f"/user/passwordResetConfirm/{uid}/{token}",
            {"password": "testpassword", "confirm-password": "testpassword"},
        )
        self.assertRedirects(
            response=response,
            expected_url="/user/login/",
            status_code=302,
            target_status_code=200,
        )

        print("\nCompleted: test for checking password reset of existing user")

    def test_02_invalid_token(self):
        print(
            "\nRunning: test for checking password reset of existing user with invalid token"
        )

        response = self.client.post(
            "/user/passwordReset/", {"user_email": self.user_email}
        )
        self.assertRedirects(
            response=response,
            expected_url="/user/login/",
            status_code=302,
            target_status_code=200,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.SUCCESS])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, PASSWORD_RESET_SUBJECT)
        msgs = str(mail.outbox[0].message()).splitlines()
        for msg in msgs:
            if msg.startswith("http://"):
                uid = msg.split("/")[-2]

        response = self.client.post(
            f"/user/passwordResetConfirm/{uid}/invalid_password",
            {"password": "testpassword", "confirm-password": "testpassword"},
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.ERROR])
        self.assertRedirects(
            response=response,
            expected_url="/user/passwordReset/",
            status_code=302,
            target_status_code=200,
        )

        print(
            "\nCompleted: test for checking password reset of existing user with invalid token"
        )

    def test_03_nonexisting_user(self):
        print("\nRunning: test for checking password reset of nonexisting user")

        response = self.client.post(
            "/user/passwordReset/", {"user_email": "invalid_email"}
        )
        self.assertRedirects(
            response=response,
            expected_url="/user/registration/",
            status_code=302,
            target_status_code=200,
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.ERROR])
        self.assertEqual(len(mail.outbox), 0)

        print("\nCompleted: test for checking password reset of nonexisting user")
