from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import Patient
from doctor.models import Doctor
from hospital.models import HospitalAdmin, Hospital
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
            borough="BKN",
            zip="54321",
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpassword"
        )

        # test cases for new account version to validate different user types
        self.userH = User.objects.create_user(
            username="testHospitalAdmin@example.com",
            password="testpassword",
            email="testHospitalAdmin@example.com",
        )

        self.userD = User.objects.create_user(
            username="testDoctor@example.com",
            password="testpassword",
            email="testDoctor@example.com",
        )

        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            facility_type="Test Facility",
            borough="Borough",
            phone="1234567890",
            location="Test Location",
            postal_code=54321,
        )

        self.hospital_admin = HospitalAdmin.objects.create(
            email="testHospitalAdmin@example.com",
            name="Test Hospital Admin",
            phone="1234567890",
            address="123 Street",
            borough="Borough",
            zip="54321",
            associated_hospital=self.hospital,
        )

        self.doctor = Doctor.objects.create(
            email="testDoctor@example.com",
            name="Test Doctor",
            phone="1234567890",
            address="123 Street",
            borough="Borough",
            zip="54321",
            primary_speciality="Test Speciality",
            associated_hospital=self.hospital,
        )

    def test_authenticated_user_can_access_account_view(self):
        print("\nRunning: test for user autentication")
        self.client.login(username="testuser@example.com", password="testpassword")
        response = self.client.get(reverse("user:account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/account.html")
        print("Completed: test for user autentication")

    def test_authenticated_hospital_admin_can_access_account_view(self):
        print("\nRunning: test for hospital admin accessing account view")
        self.client.login(
            username="testHospitalAdmin@example.com", password="testpassword"
        )
        response = self.client.get(reverse("user:account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/account.html")
        print("Completed: test for hospital admin accessing account view")

    def test_authenticated_doctor_can_access_account_view(self):
        print("\nRunning: test for doctor accessing account view")
        self.client.login(username="testDoctor@example.com", password="testpassword")
        response = self.client.get(reverse("user:account"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/account.html")
        print("Completed: test for doctor accessing account view")

    def test_authenticated_user_can_update_account_info(self):
        print("\nRunning: test for user account edit")
        self.client.login(username="testuser@example.com", password="testpassword")
        updated_data = {
            "email": "testuser@example.com",
            "name": "Updated User",
            "phone": "9876543210",
            "sex": "male",
            "address": "123 Updated Street",
            "borough": "BKN",
            "zip": "54321",
        }

        response = self.client.post(reverse("user:account"), data=updated_data)

        # check if the user info is updated
        updated_user = Patient.objects.get(email="testuser@example.com")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_user.name, updated_data["name"])
        print("Completed: test for user account edit")

    @override_settings(MEDIA_ROOT=settings.MEDIA_ROOT)
    def test_upload_avatar_within_allowed_size(self):
        self.client.login(username="testuser@example.com", password="testpassword")

        # Create a file with size less than the allowed limit (50KB)
        desired_size_kb = 49
        desired_size_bytes = desired_size_kb * 1024  # Convert KB to bytes

        # Calculate the number of repetitions needed to achieve the desired size
        repetitions = desired_size_bytes // len(b"file_content")

        # Create the byte sequence
        avatar_content = b"file_content" * repetitions

        avatar = SimpleUploadedFile(
            "test-avatar.png", avatar_content, content_type="image/png"
        )

        response = self.client.post(reverse("user:account"), {"avatar": avatar})
        self.assertEqual(response.status_code, 302)
        self.patient.refresh_from_db()
        self.assertIsNotNone(self.patient.avatar)

    @override_settings(MEDIA_ROOT=settings.MEDIA_ROOT)
    def test_upload_avatar_exceeds_allowed_size(self):
        self.client.login(username="testuser@example.com", password="testpassword")

        # Create a file with size more than the allowed limit (51KB)
        desired_size_kb = 51
        desired_size_bytes = desired_size_kb * 1024  # Convert KB to bytes

        # Calculate the number of repetitions needed to achieve the desired size
        repetitions = desired_size_bytes // len(b"file_content")

        # Create the byte sequence
        avatar_content = b"file_content" * repetitions
        avatar = SimpleUploadedFile(
            "test-avatar.png", avatar_content, content_type="image/png"
        )

        response = self.client.post(reverse("user:account"), {"avatar": avatar})

        # Check if the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode("utf-8"),
            "File size is too large. Maximum allowed size is 50 KB.",
        )

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
