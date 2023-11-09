from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from user.models import Patient
from doctor.models import Doctor, DoctorAppointment
from hospital.models import Hospital, HospitalAppointment


class AppointmentViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a patient
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

        # Create a doctor
        self.doctor_user = User.objects.create_user(
            username="testdoctor@example.com",
            password="testpassword",
            email="testdoctor@example.com",
        )
        self.doctor = Doctor.objects.create(
            email="testdoctor@example.com",
            name="Test Doctor",
            phone="9876543210",
            address="456 Avenue",
            borough="MHT",
            zip="12345",
            primary_speciality="General Medicine",
        )

        # Create a hospital
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

        # Create doctor appointment associated with the created doctor
        self.doctor_appointment = DoctorAppointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            start_time="2023-12-01T12:00:00Z",
            name="Test Appointment",
            phone="1234567890",
            email="test@example.com",
            reason="Test Reason",
            status="REQ",
        )

        # Create hospital appointment associated with the created hospital
        self.hospital_appointment = HospitalAppointment.objects.create(
            hospital=self.hospital,
            patient=self.patient,
            start_time="2023-12-01T12:00:00Z",
            name="Test Hospital Appointment",
            phone="1234567890",
            email="test@example.com",
            reason="Test Reason",
            status="REQ",
        )

    def test_cancel_doctor_appointment(self):
        print("\nRunning: test cancel doctor appointment")
        self.client.login(username="testuser@example.com", password="testpassword")
        response = self.client.post(
            reverse("user:cancelAppointment"),
            {
                "appointment_id": self.doctor_appointment.id,
                "appointment_type": "consultation",
                "operation": "CCL",
                "cancel_reason": "Test Reason for Cancellation",
            },
        )
        self.assertEqual(response.status_code, 302)
        updated_appointment = DoctorAppointment.objects.get(
            id=self.doctor_appointment.id
        )
        self.assertEqual(updated_appointment.status, "CCL")
        self.assertEqual(updated_appointment.cancel_msg, "Test Reason for Cancellation")
        print("Completed: test cancel doctor appointment")

    def test_confirm_hospital_appointment(self):
        print("\nRunning: test confirm hospital appointment")
        self.client.login(username="testuser@example.com", password="testpassword")
        response = self.client.post(
            reverse("user:confirmAppointment"),
            {
                "appointment_id": self.hospital_appointment.id,
                "appointment_type": "hospital",
                "operation": "CNF",
            },
        )
        self.assertEqual(response.status_code, 302)
        updated_appointment = HospitalAppointment.objects.get(
            id=self.hospital_appointment.id
        )
        self.assertEqual(updated_appointment.status, "CNF")
        print("Completed: test confirm hospital appointment")

    def tearDown(self):
        self.doctor_appointment.delete()
        self.hospital_appointment.delete()
        self.patient.delete()
        self.user.delete()
        self.doctor_user.delete()
        self.hospital.delete()
        self.doctor.delete()
