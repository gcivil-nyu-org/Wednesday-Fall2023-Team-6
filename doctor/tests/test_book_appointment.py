import json

from django.test import TestCase, Client
from django.urls import reverse
from doctor.models import Doctor, DoctorAppointment
from user.models import Patient


class BookConsultationTestCase(TestCase):
    def setUp(self):
        # Set up data for the whole TestCase
        self.client = Client()
        self.doctor = Doctor.objects.create(
            name="Dr. Jane Smith",
            email="dr.jane.smith@example.com",
            phone="123-456-7890",
            sex="Female",
            address="123 Wellness Way",
            borough="Manhattan",
            zip="10001",
            primary_speciality="Cardiology",
            # Add other fields as needed for Doctor model
        )
        self.patient = Patient.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            phone="123-456-7890",
            sex="male",
            address="123 Test St",
            borough="MHT",
            zip=10001,
            insurance_provider="ABC Insurance",
        )
        saved_patient = Patient.objects.get(pk=self.patient.pk)
        print({self.patient.id})
        response = self.client.get(f'/doctor/{self.doctor.id}/')
        print(response)
        self.book_consultation_url = f'/doctor/{self.doctor.id}/bookConsultation/'
        self.data = {
            "date": "2023-11-03",
            "time": "05:43",
            "name": "Test User",
            "phone": "1234567890",
            "email": "test@example.com",
            "reason": "Test reason for visit",
        }

    def test_book_consultation(self):
        # Test booking a consultation successfully
        response = self.client.post(self.book_consultation_url, json.dumps(self.data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DoctorAppointment.objects.count(), 1)
        appointment = DoctorAppointment.objects.first()
        self.assertEqual(appointment.name, "Test User")
        self.assertEqual(appointment.phone, "1234567890")
        self.assertEqual(appointment.email, "test@example.com")
        self.assertEqual(appointment.reason, "Test reason for visit")
        self.assertTrue(appointment.start_time)

    def test_book_consultation_invalid_data(self):
        # Test booking a consultation with invalid data
        self.data.pop("email")  # Remove email to simulate invalid data
        response = self.client.post(
            self.book_consultation_url, self.data, content_type="text/html"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(DoctorAppointment.objects.count(), 0)

    def test_book_consultation_no_doctor(self):
        # Test booking a consultation with a non-existent doctor
        wrong_url = reverse("doctor:book_consultation", kwargs={"doctor_id": 999})
        response = self.client.post(wrong_url, self.data, content_type="text/html")
        self.assertEqual(response.status_code, 404)
    def test_book_consultation_no_patient(self):
        self.patient.delete()
        # Test booking a consultation successfully
        response = self.client.post(self.book_consultation_url, json.dumps(self.data), content_type="application/json")
        self.assertEqual(response.status_code, 404)

