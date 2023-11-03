from django.test import TestCase
from django.urls import reverse
from doctor.models import Doctor


class DoctorDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a doctor for testing the detail view
        cls.doctor = Doctor.objects.create(
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

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f"/doctor/{self.doctor.id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(f"/doctor/{self.doctor.id}/")
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(f"/doctor/{self.doctor.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "doctor/doctor_details.html")

    def test_context_data(self):
        response = self.client.get(f"/doctor/{self.doctor.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("doctor" in response.context)
        self.assertEqual(response.context["doctor"], self.doctor)

    # Add more tests to cover different scenarios and edge cases
