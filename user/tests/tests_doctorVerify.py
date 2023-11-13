from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from doctor.models import Doctor
from hospital.models import Hospital, HospitalAdmin
from unittest.mock import patch


class AssociateDoctorViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a hospital and a doctor associated with the hospital
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            facility_type="General",
            borough="MHT",
            phone="1112223333",
            location="789 Street",
            postal_code=67890,
            latitude=40.7128,
            longitude=-74.0060,
        )

        self.doctor = Doctor.objects.create(
            email="testdoctor@example.com",
            name="Test Doctor",
            phone="9876543210",
            address="456 Avenue",
            borough="MHT",
            zip="12345",
            primary_speciality="General Medicine",
            associated_hospital=self.hospital,
            active_status=False,  # Set active_status to False initially
        )

        # Create a hospital admin user
        self.hospital_admin_user = User.objects.create_user(
            username="testadmin@example.com",
            password="testpassword",
            email="testadmin@example.com",
        )

        self.hospital_admin = HospitalAdmin.objects.create(
            email="testadmin@example.com",
            name="Test Admin",
            phone="1234567890",
            address="123 Street",
            borough="MHT",
            zip="54321",
            associated_hospital=self.hospital,
        )

    def test_approve_doctor(self):
        print("\nRunning: test approve doctor")
        self.client.login(username="testadmin@example.com", password="testpassword")

        response = self.client.post(
            reverse("user:associate_doctor"),
            {"doctor_id": self.doctor.id, "decision": "APPROVE"},
        )

        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.doctor.refresh_from_db()
        self.assertTrue(
            self.doctor.active_status
        )  # Assert that active_status is now True
        print("Completed: test approve doctor")

    @patch("user.views.send_email")
    def test_reject_doctor_with_email_failure(self, mock_send_email):
        print("\nRunning: test reject doctor with email failure")
        mock_send_email.return_value = False  # Simulate email failure
        self.client.login(username="testadmin@example.com", password="testpassword")

        response = self.client.post(
            reverse("user:associate_doctor"),
            {
                "doctor_id": self.doctor.id,
                "decision": "REJECT",
                "cancel_reason": "Test Reject Reason",
            },
        )

        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.doctor.refresh_from_db()
        self.assertFalse(
            self.doctor.active_status
        )  # Assert active_status is still False
        print("Completed: test reject doctor with email failure")

    @patch("user.views.send_email")
    def test_reject_doctor_with_email_success(self, mock_send_email):
        print("\nRunning: test reject doctor with email success")
        mock_send_email.return_value = True  # Simulate email success
        self.client.login(username="testadmin@example.com", password="testpassword")

        response = self.client.post(
            reverse("user:associate_doctor"),
            {
                "doctor_id": self.doctor.id,
                "decision": "REJECT",
                "cancel_reason": "Test Reject Reason",
            },
        )

        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.doctor.refresh_from_db()
        self.assertIsNone(
            self.doctor.associated_hospital
        )  # Assert associated_hospital is None
        self.assertTrue(self.doctor.active_status)  # Assert active_status is still True
        print("Completed: test reject doctor with email success")

    def tearDown(self):
        self.doctor.delete()
        self.hospital_admin.delete()
        self.hospital.delete()
        self.hospital_admin_user.delete()
