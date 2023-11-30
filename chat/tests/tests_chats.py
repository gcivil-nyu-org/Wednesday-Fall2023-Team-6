import os
import shutil
import tempfile
from unittest.mock import patch, MagicMock
import datetime

from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from chat.models import Message
from doctor.models import Doctor, DoctorAppointment
from hospital.models import Hospital, HospitalAdmin
from user.models import Patient


class BaseChatViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a patient user
        self.user = User.objects.create_user(
            username="testuser@example.com",
            password="testpassword",
            email="testuser@example.com",
        )

        self.patient = Patient.objects.create(
            email="testuser@example.com",
            name="Test User",
            zip="54321",
        )

        # Create a doctor user
        self.doctor_user = User.objects.create_user(
            username="testdoctor@example.com",
            password="testpassword",
            email="testdoctor@example.com",
        )
        self.doctor = Doctor.objects.create(
            email="testdoctor@example.com",
            name="Test Doctor",
            zip="12345",
        )

        # Create an hospitalAdmin user
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

        # Create an appointment
        self.appointment = DoctorAppointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            status="REQ",  # Pending status
            start_time=datetime.datetime.now(),
        )

        # User login
        self.client.login(username="testuser@example.com", password="testpassword")

        # Temporary media root for file uploads
        self.temp_media_root = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_media_root)


class TestAppointmentStatus(BaseChatViewTest):
    def test_appointment_not_confirmed(self):
        response = self.client.get(reverse("chat:chat", args=(self.appointment.id,)))
        self.assertRedirects(
            response, reverse("user:account"), status_code=302, target_status_code=200
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Error: Appointment not confirmed.")

    def test_appointment_not_started(self):
        self.appointment.start_time = datetime.datetime.now() + datetime.timedelta(
            days=1
        )
        self.appointment.status = "CNF"
        self.appointment.save()
        response = self.client.get(reverse("chat:chat", args=(self.appointment.id,)))
        self.assertRedirects(
            response, reverse("user:account"), status_code=302, target_status_code=200
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Error: Appointment not started yet")


class TestMessageRetrievalAndDisplay(BaseChatViewTest):
    @patch("chat.views.Message.objects.filter")
    def test_message_retrieval_and_display(self, mock_filter):
        self.appointment.start_time = datetime.datetime.now()
        self.appointment.status = "CNF"
        self.appointment.save()
        mock_query_set = MagicMock()
        mock_query_set.order_by.return_value = [
            Message(content="Test message", appointment=self.appointment)
        ]
        mock_filter.return_value = mock_query_set
        response = self.client.get(reverse("chat:chat", args=(self.appointment.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            any("Test message" in m.content for m in response.context["messages"])
        )


class TestPostAttachment(BaseChatViewTest):
    def test_post_attachment(self):
        self.appointment.start_time = datetime.datetime.now()
        self.appointment.status = "CNF"
        self.appointment.save()
        url = reverse("chat:chat", args=[self.appointment.id])
        mock_file = SimpleUploadedFile(
            "file.txt", b"file_content", content_type="text/plain"
        )
        data = {"content": "test message", "attachment": mock_file}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(content="test message").exists())
        message = Message.objects.get(content="test message")
        self.assertTrue(message.attachment.name.endswith(".txt"))
        self.assertTrue(os.path.exists(message.attachment.path))
        message.attachment.delete()  # Clean up


class TestLogoutUserAccess(BaseChatViewTest):
    def test_logout_user_access(self):
        self.client.logout()
        response = self.client.get(reverse("chat:chat", args=(self.appointment.id,)))
        expected_redirect_url = f"{reverse('user:login')}?next={reverse('chat:chat', args=(self.appointment.id,))}"
        self.assertRedirects(
            response, expected_redirect_url, status_code=302, target_status_code=200
        )


class TestDoctorUserAccess(BaseChatViewTest):
    def test_doctor_user_access(self):
        self.client.login(username="testdoctor@example.com", password="testpassword")
        response = self.client.get(reverse("chat:chat", args=(self.appointment.id,)))
        self.assertEqual(response.status_code, 302)


class TestHospitalAdminAccess(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a patient user
        self.user = User.objects.create_user(
            username="testuser@example.com",
            password="testpassword",
            email="testuser@example.com",
        )

        self.patient = Patient.objects.create(
            email="testuser@example.com",
            name="Test User",
            zip="54321",
        )

        # Create a doctor user
        self.doctor_user = User.objects.create_user(
            username="testdoctor@example.com",
            password="testpassword",
            email="testdoctor@example.com",
        )
        self.doctor = Doctor.objects.create(
            email="testdoctor@example.com",
            name="Test Doctor",
            zip="12345",
        )

        # Create an hospitalAdmin user
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

        # Create an appointment
        self.appointment = DoctorAppointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            status="CNF",  # Pending status
            start_time=datetime.datetime.now(),
        )

        # Temporary media root for file uploads
        self.temp_media_root = tempfile.mkdtemp()

    def test_hospitalAdmin_access(self):
        self.client.login(username="testadmin@example.com", password="testpassword")
        response = self.client.get(reverse("chat:chat", args=(self.appointment.id,)))
        self.assertRedirects(
            response, reverse("user:account"), status_code=302, target_status_code=200
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Unauthorized User")
