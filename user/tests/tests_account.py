from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import Patient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.test import override_settings
from MediLink import settings


class AccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser@example.com",
            password="testpassword",
            email="testuser@example.com",
        )
        self.patient = Patient.objects.create(
            email="testuser@example.com",
            name="Test User",
            phone="1234567890",
            address="123 Street",
            borough="Borough",
            zip="54321",
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpassword"
        )

    def test_authenticated_user_can_access_account_view(self):
        print("\nRunning: test for user autentication")
        self.client.login(username="testuser@example.com", password="testpassword")
        response = self.client.get(reverse("user:account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/account.html")
        print("Completed: test for user autentication")

    def test_authenticated_user_can_update_account_info(self):
        print("\nRunning: test for user account edit")
        self.client.login(username="testuser@example.com", password="testpassword")
        updated_data = {
            "email": "testuser@example.com",
            "name": "Updated User",
            "phone": "9876543210",
            "sex": "Male",
            "address": "123 Updated Street",
            "borough": "Updated Borough",
            "zip": "54321",
        }

        response = self.client.post(reverse("user:account"), data=updated_data)

        # check if the user info is updated
        updated_user = Patient.objects.get(email="testuser@example.com")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_user.name, updated_data["name"])
        print("Completed: test for user account edit")

    @override_settings(MEDIA_ROOT=settings.MEDIA_ROOT)
    def test_upload_avatar(self):
        self.client.login(username="testuser@example.com", password="testpassword")
        avatar = SimpleUploadedFile(
            "test-avatar.png", b"file_content", content_type="image/png"
        )
        response = self.client.post(reverse("user:account"), {"avatar": avatar})
        self.assertEqual(response.status_code, 302)
        self.patient.refresh_from_db()
        self.assertIsNotNone(self.patient.avatar)

    # delete test avatars
    def tearDown(self):
        # Delete the test avatars after the test is complete
        if self.patient.avatar:
            default_storage.delete(self.patient.avatar.name)

    def test_admin_user_redirected_to_admin_page(self):
        print("\nRunning: test for admin user redirect")
        self.client.login(username="admin", password="adminpassword")
        response = self.client.get(reverse("user:account"))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(
            response.url, reverse("admin:index")
        )  # Check if the admin is redirected to admin page
        print("Completed: test for admin user redirect")

    def test_unauthenticated_user_redirected_to_login_page(self):
        print("\nRunning: test for unauthenticated user")
        response = self.client.get(reverse("user:account"))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(
            response.url, reverse("user:login")
        )  # Check if the user is redirected to login page
        print("Completed: test for unauthenticated user")
