from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.messages import get_messages, constants
from user.models import Patient
from doctor.models import Doctor
from hospital.models import HospitalAdmin, Hospital

from MediLink.settings import MESSAGE_TAGS


class RegistrationTests(TestCase):
    @classmethod
    def setUpClass(self):
        # Create Patient
        self.patient_user_email = "test_patient_user@gmail.com"
        self.user_password = "test_password"

        # Create Doctor
        self.doctor_user_email = "test_doctor_user@gmail.com"

        # Create Hospital Admin
        self.admin_user_email = "test_admin_user@gmail.com"

        self.hosiptal = Hospital.objects.create(
            name="Test",
            facility_type="Test",
            borough="Test",
            phone="34536",
            location="Test",
            postal_code=12345,
        )

        self.post_data_patient = {
            "user_email": self.patient_user_email,
            "user_name": "Patient",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "patient",
            "address": "73rd Street",
            "borough": "BKN",
            "zip": 11209,
            "insurance": "NYU Insurance",
        }

        self.post_data_doctor = {
            "user_email": self.doctor_user_email,
            "user_name": "Doctor",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "doctor",
            "address": "73rd Street",
            "borough": "BKN",
            "zip": 11209,
            "specialization": "Pediatrician",
            "hospital": "",
        }

        self.post_data_hospital = {
            "user_email": self.admin_user_email,
            "user_name": "Hospital",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "hospital-admin",
            "address": "73rd Street",
            "borough": "BKN",
            "zip": 11209,
            "hospital": self.hosiptal.id,
        }

        User.objects.create_user(
            self.patient_user_email, self.patient_user_email, self.user_password
        )
        User.objects.create_user(
            self.doctor_user_email, self.doctor_user_email, self.user_password
        )
        User.objects.create_user(
            self.admin_user_email, self.admin_user_email, self.user_password
        )

    def test_01_nonexisting_user(self):
        print("\nRunning: test for checking registration of nonexisting user")

        post_data_users = [
            dict(self.post_data_patient),
            dict(self.post_data_doctor),
            dict(self.post_data_hospital),
        ]

        for post_data in post_data_users:
            post_data["user_email"] += ".in"  # So that user is new and non-existing
            response = self.client.post("/user/registration/", post_data)
            messages = list(get_messages(response.wsgi_request))
            if len(messages) > 0:
                print("Error Message::")
                print(messages[0].message)

            self.assertTrue(User.objects.filter(email=post_data["user_email"]).exists())
            if post_data["userType"] == "patient":
                self.assertTrue(
                    Patient.objects.filter(email=post_data["user_email"]).exists()
                )
                user = Patient.objects.get(email=post_data["user_email"])
            elif post_data["userType"] == "doctor":
                self.assertTrue(
                    Doctor.objects.filter(email=post_data["user_email"]).exists()
                )
                user = Doctor.objects.get(email=post_data["user_email"])
            else:
                self.assertTrue(
                    HospitalAdmin.objects.filter(email=post_data["user_email"]).exists()
                )
                user = HospitalAdmin.objects.get(email=post_data["user_email"])

            self.assertEqual(user.name, post_data["user_name"])
            self.assertEqual(user.sex.lower(), str(post_data["user_sex"]).lower())
            self.assertEqual(user.phone, post_data["user_phone"])

            self.assertEqual(user.borough, post_data["borough"])
            self.assertEqual(user.address, post_data["address"])
            self.assertEqual(user.zip, post_data["zip"])

            if post_data["userType"] == "patient":
                self.assertEqual(user.insurance_provider, post_data["insurance"])
            elif post_data["userType"] == "doctor":
                self.assertEqual(user.primary_speciality, post_data["specialization"])
                self.assertEqual(user.associated_hospital, None)
            else:
                self.assertEqual(user.associated_hospital.id, post_data["hospital"])

            logged_in_user = auth.get_user(self.client)
            self.assertEqual(logged_in_user.get_username(), post_data["user_email"])
            self.assertTrue(logged_in_user.is_authenticated)
            self.assertRedirects(
                response=response,
                expected_url="/user/home/",
                status_code=302,
                target_status_code=200,
            )
            self.client.logout()

        # Replace with our logout call later
        print("Completed: test for checking login of nonexisting user")

    def test_02_existing_user_all_data(self):
        print("\nRunning: test for checking registration of existing users")

        post_data_users = [
            self.post_data_patient,
            self.post_data_doctor,
            self.post_data_hospital,
        ]

        for post_data in post_data_users:
            response = self.client.post("/user/registration/", post_data)
            logged_in_user = auth.get_user(self.client)
            self.assertNotEqual(logged_in_user.get_username(), post_data["user_email"])
            self.assertFalse(logged_in_user.is_authenticated)
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.ERROR])
            self.assertRedirects(
                response=response,
                expected_url="/user/registration/",
                status_code=302,
                target_status_code=200,
            )

        # Replace with our logout call later
        print("Completed: test for checking registration of existing users")

    def test_03_nonexisting_user_incorrect_data(self):
        print("\nRunning: test for checking registration of incorrect users")
        post_invalid_email = {
            "user_email": "invalid",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "patient",
            "address": "73rd Street",
            "borough": "BKN",
            "zip": 11209,
        }

        post_invalid_name = {
            "user_email": "valid@gmail.com",
            "user_name": "",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "patient",
            "address": "73rd Street",
            "borough": "BKN",
            "zip": 11209,
        }

        post_invalid_password = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": "",
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "patient",
            "address": "73rd Street",
            "borough": "BKN",
            "zip": 11209,
        }

        post_invalid_sex = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "gmale",
            "user_phone": "1234567890",
            "userType": "patient",
            "address": "73rd Street",
            "borough": "BKN",
            "zip": 11209,
        }

        post_invalid_phone = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "",
            "userType": "patient",
            "address": "73rd Street",
            "borough": "BKN",
            "zip": 11209,
        }

        post_invalid_type = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "none",
            "address": "73rd Street",
            "borough": "BKN",
            "zip": 11209,
        }

        post_invalid_borough = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "patient",
            "address": "73rd Street",
            "borough": "Brooklyn",
            "zip": 11209,
            "specialization": "Pediatrician",
        }

        post_invalid_hospital = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "hospital-admin",
            "address": "73rd Street",
            "borough": "Brooklyn",
            "zip": 11209,
            "hospital": "",
        }

        post_data_users = [
            post_invalid_email,
            post_invalid_name,
            post_invalid_password,
            post_invalid_sex,
            post_invalid_phone,
            post_invalid_type,
            post_invalid_borough,
            post_invalid_hospital,
        ]

        for post_data in post_data_users:
            response = self.client.post("/user/registration/", post_data)
            logged_in_user = auth.get_user(self.client)
            self.assertNotEqual(logged_in_user.get_username(), post_data["user_email"])
            self.assertFalse(logged_in_user.is_authenticated)
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.ERROR])
            self.assertRedirects(
                response=response,
                expected_url="/user/registration/",
                status_code=302,
                target_status_code=200,
            )

        # Replace with our logout call later
        print("Completed: test for checking registration of incorrect users")

    def tearDown(self):
        self.client.logout()

    @classmethod
    def tearDownClass(self):
        self.hosiptal.delete()
