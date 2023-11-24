import os
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
from PIL import Image


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
            primary_speciality="Family Medicine",
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

        # Calculate the number of bytes required for the desired file size
        file_size_bytes = 10 * 1024 * 1024
        # Calculate the dimensions to achieve the desired file size (for simplicity, a square image is created)
        side_length = int(
            (file_size_bytes**0.5) / 3
        )  # Dividing by 3 to approximate RGB channels
        image = Image.new("RGB", (side_length, side_length), "white")
        image_path = "test_image.jpg"
        image.save(image_path)

        with open(image_path, "rb") as f:
            avatar = SimpleUploadedFile(
                "test_image.jpg", f.read(), content_type="image/jpeg"
            )

        response = self.client.post(reverse("user:account"), {"avatar": avatar})
        self.assertRedirects(
            response=response,
            expected_url="/user/account/",
            status_code=302,
            target_status_code=200,
        )
        self.patient.refresh_from_db()
        self.assertIsNotNone(self.patient.avatar)
        os.remove("test_image.jpg")

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

    def test_associated_hospital_logic(self):
        print("\nRunning: test_associated_hospital_logic")
        self.client.login(
            username="testHospitalAdmin@example.com", password="testpassword"
        )

        new_hospital = Hospital.objects.create(
            name="New Hospital",
            facility_type="Test Facility",
            borough="Borough",
            phone="1234567890",
            location="Test Location",
            postal_code=54321,
        )

        # Provide an empty string for associated hospital name
        updated_data = {
            "email": "testHospitalAdmin@example.com",
            "name": "Updated Hospital Admin",
            "phone": "9876543210",
            "sex": "male",
            "address": "123 Updated Street",
            "borough": "BKN",
            "zip": "54321",
            "user_type": "hospital-admin",
            "associatedHospital": "DNE",  # Empty string for associated hospital
        }

        response = self.client.post(reverse("user:account"), data=updated_data)
        self.assertEqual(response.status_code, 302)
        # Check if the associated hospital is still the same

        self.assertEqual(
            HospitalAdmin.objects.get(
                email="testHospitalAdmin@example.com"
            ).associated_hospital.name,
            "Test Hospital",
        )

        # Provide another existing hospital
        updated_data2 = {
            "email": "testHospitalAdmin@example.com",
            "name": "Updated Hospital Admin",
            "phone": "9876543210",
            "sex": "male",
            "address": "123 Updated Street",
            "borough": "BKN",
            "zip": "54321",
            "user_type": "hospital-admin",
            "associatedHospital": "New Hospital",  # Empty string for associated hospital
            "hospital": new_hospital.id,
        }

        response = self.client.post(reverse("user:account"), data=updated_data2)
        self.assertEqual(response.status_code, 302)
        # Check response status

        self.assertFalse(
            HospitalAdmin.objects.get(
                email="testHospitalAdmin@example.com"
            ).active_status
        )

        print("Completed: test_associated_hospital_logic")

    def test_user_validity_check_and_update(self):
        print("\nRunning: test user validity check and update")
        self.client.login(username="testDoctor@example.com", password="testpassword")

        # Test with valid data
        valid_data = {
            "email": "testDoctor@example.com",
            "name": "Updated Doctor",
            "specialization": "Updated Speciality",
            "user_type": "doctor",
            "associatedHospital": "Test Hospital",
            "hospital": self.hospital.id,
            "phone": "9876543210",
            "sex": "male",
            "address": "123 Updated Street",
            "borough": "BKN",
            "zip": "54321",
        }

        response = self.client.post(reverse("user:account"), data=valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Doctor.objects.get(email="testDoctor@example.com").name, "Updated Doctor"
        )
        # Test with invalid data
        invalid_data = {
            "email": "testDoctor@example.com",
            "name": "Updated Doctor 2",
            "phone": "9876543210",
            "sex": "male",
            "user_type": "doctor",
            "specialization": "Updated Speciality",
            "associatedHospital": "invalid hospital",
            "address": "123 Updated Street",
            "borough": "BKN",
            "zip": "54321",
        }
        response = self.client.post(reverse("user:account"), data=invalid_data)
        self.assertEqual(response.status_code, 302)
        # Check if an error message is displayed or handle it based on your actual implementation
        self.assertEqual(
            Doctor.objects.get(email="testDoctor@example.com").associated_hospital.name,
            self.hospital.name,
        )

        # Test with no hospital name
        invalid_data = {
            "email": "testDoctor@example.com",
            "name": "Updated Doctor 2",
            "phone": "9876543210",
            "sex": "male",
            "user_type": "doctor",
            "specialization": "Updated Speciality",
            "associatedHospital": "",
            "address": "123 Updated Street",
            "borough": "BKN",
            "zip": "54321",
        }
        response = self.client.post(reverse("user:account"), data=invalid_data)
        self.assertEqual(response.status_code, 302)
        # Check if an error message is displayed or handle it based on your actual implementation
        self.assertIsNone(
            Doctor.objects.get(email="testDoctor@example.com").associated_hospital
        )

        print("Completed: test user validity check and update")
