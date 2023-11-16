from django.test import TestCase, Client
from django.urls import reverse
from hospital.models import Hospital, HospitalAppointment
from user.models import Patient
from doctor.models import Doctor
from django.contrib.auth.models import User
import json


class BookAppointmentViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(
            username="testuser@example.com",
            password="testpassword",
            email="testuser@example.com",
        )

        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            facility_type="Type A",
            borough="BKN",
            phone="123-456-7890",
            location="Location A",
            postal_code=12345,
        )

        self.doctor = Doctor.objects.create(
            name="Doctor B",
            email="doctorB@example.com",
            phone="987-654-3210",
            sex="Female",
            address="Test Address B",
            borough="Queens",
            zip=54321,
            primary_speciality="Dermatology",
        )

        self.patient = Patient.objects.create(
            email="testuser@example.com",
            name="Test User",
            phone="1234567890",
            address="123 Street",
            borough="Borough",
            zip="54321",
        )

        self.login_url = reverse("user:login")

        self.appointment_data = {
            "date": "2023-01-01",
            "time": "10:00",
            "preferred_doctor": self.doctor.id,
            "name": "Test Patient",
            "phone": "1234567890",
            "email": "test@example.com",
            "reason": "Test reason",
            "accebility": "all good",
        }

    def test_book_appointment_authenticated_user(self):
        print("\nRunning: test for authenticated user")

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("hospital:book_appointment", args=[self.hospital.id]),
            json.dumps(self.appointment_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(HospitalAppointment.objects.count(), 1)
        self.assertEqual(HospitalAppointment.objects.first().patient, self.patient)
        self.assertEqual(HospitalAppointment.objects.first().hospital, self.hospital)

        print("\nCompleted: test for authenticated user")

    def test_book_appointment_unauthenticated_user(self):
        print("\nRunning: test for unauthenticated user")
        response = self.client.post(
            reverse("hospital:book_appointment", args=[self.hospital.id]),
            json.dumps(self.appointment_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(HospitalAppointment.objects.count(), 0)

    print("\nCompleted: test for unauthenticated user")

    def test_book_appointment_invalid_request(self):
        print("\nRunning: test for invalid request")
        invalid_data = {
            "date": "invalid-date",
            "time": "invalid-time",
            "preferred_doctor": self.doctor.id,
            "name": "Test Patient",
            "phone": "1234567890",
            "email": "test@example.com",
            "reason": "Test reason",
            "accebility": "all good",
        }
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("hospital:book_appointment", args=[self.hospital.id]),
            json.dumps(invalid_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(HospitalAppointment.objects.count(), 0)
        print("\nCompleted: test for invalid request")

    # def test_book_appointment_overlap(self):
    #     overlapping_appointment_time = timezone.now() + timedelta(hours=1)
    #     HospitalAppointment.objects.create(
    #         patient=self.user,
    #         hospital=self.hospital,
    #         start_time=overlapping_appointment_time,
    #     )
    #     self.client.force_login(self.user)
    #     response = self.client.post(
    #         reverse("hospital:book_appointment", args=[self.hospital.id]),
    #         json.dumps(self.appointment_data),
    #         content_type="application/json",
    #     )
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(HospitalAppointment.objects.count(), 1)
