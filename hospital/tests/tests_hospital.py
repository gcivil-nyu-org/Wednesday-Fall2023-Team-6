from django.test import TestCase
from django.urls import reverse
from hospital.models import Hospital

# from hospital.views import HospitalListView, HospitalDetailView, book_appointment
# from django.contrib.auth.models import User
# from doctor.models import Doctor
# import json


class CustomLogicTest(TestCase):
    def test_custom_logic(self):
        pass
        # Write test cases for your custom application logic
        # Ensure to test both success and error cases.


class HospitalListViewTest(TestCase):
    def test_hospital_filtering(self):
        # Create a test Hospital
        Hospital.objects.create(
            name="Test Hospital",
            facility_type="Type A",
            borough="BKN",
            phone="123-456-7890",
            location="Location A",
            postal_code=12345,
        )

        # Perform a search with a filter form
        response = self.client.get(
            reverse("hospital:list_view"), {"name": "Test Hospital"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Hospital")


class BookAppointmentViewTest(TestCase):
    def test_invalid_appointment_booking(self):
        # Create a test Hospital
        hospital = Hospital.objects.create(
            name="Test Hospital",
            facility_type="Type A",
            borough="BKN",
            phone="123-456-7890",
            location="Location A",
            postal_code=12345,
        )

        # Attempt to book an appointment with invalid data
        response = self.client.post(
            reverse("hospital:book_appointment", args=[hospital.id]),
            {
                "date": "2023-11-03",
                "time": "10:00",
                "name": "John Doe",
                "phone": "invalid_phone",  # Invalid phone format
                "email": "johndoe@example.com",
                "reason": "Checkup",
                "accebility": "Wheelchair access",
            },
        )

        self.assertEqual(response.status_code, 400)  # Should return a bad request


class HospitalDetailViewTest(TestCase):
    def test_hospital_detail_view(self):
        # Create a test Hospital
        hospital = Hospital.objects.create(
            name="Test Hospital",
            facility_type="Type A",
            borough="BKN",
            phone="123-456-7890",
            location="Location A",
            postal_code=12345,
        )

        response = self.client.get(reverse("hospital:detail_view", args=[hospital.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hospital/hospital_details.html")

        self.assertContains(response, "Test Hospital")

        # Add more assertions to test the view's behavior.
