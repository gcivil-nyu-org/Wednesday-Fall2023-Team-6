from django.test import TestCase
from datetime import datetime, timedelta
from hospital.models import HospitalAppointment, Hospital
from user.models import Patient
from hospital.views import check_appointment_overlap


class CheckAppointmentOverlapTest(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            email="testuser@example.com",
            name="Test User",
            phone="1234567890",
            address="123 Street",
            borough="Borough",
            zip="54321",
        )

        self.hospital = Hospital.objects.create(
            name="Hospital B",
            facility_type="Type B",
            borough="QNS",
            phone="576-293-4829",
            location="Location B",
            postal_code=54321,
        )

        self.appointment_time = datetime(2023, 1, 1, 10, 0)  # January 1, 2023, 10:00 AM

    def test_no_overlap(self):
        result, message = check_appointment_overlap(self.patient, self.appointment_time)
        self.assertFalse(result)
        self.assertEqual(message, "")

    def test_overlap_existing_appointment(self):
        # Create an appointment that overlaps with the test appointment
        overlapping_appointment_time = self.appointment_time + timedelta(minutes=15)
        HospitalAppointment.objects.create(
            hospital=self.hospital,
            patient=self.patient,
            start_time=overlapping_appointment_time,
        )

        result, message = check_appointment_overlap(self.patient, self.appointment_time)
        self.assertTrue(result)
        self.assertEqual(
            message, "You have an overlapping appointment/request at that time"
        )
