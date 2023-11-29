from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from hospital.models import Hospital
from user.models import Patient,Hospital_Reviews


class AddReviewTestCase(TestCase):
    def setUp(self):
        # Create a user with patient role
        self.patient_user = User.objects.create_user(
            username="patient@example.com", password="password"
        )
        self.patient = Patient.objects.create(
            user=self.patient_user, name="John Doe", email="patient@example.com"
        )

        # Create a hospital for testing
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            location="Test Location",
            description="Test Description",
        )

        # URL for the add_review view
        self.url = reverse("add_review", args=[self.hospital.id])

    def test_authenticated_user_can_add_review(self):
        # Log in the patient user
        self.client.login(username="patient@example.com", password="password")

        # Make a POST request to add a review
        response = self.client.post(
            self.url,
            {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
        )

        # Check that the review was added successfully
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Hospital_Reviews.objects.count(), 1)
        self.assertEqual(Hospital_Reviews.objects.first().review_from, "John Doe")

    def test_unauthenticated_user_cannot_add_review(self):
        # Make a POST request to add a review without logging in
        response = self.client.post(
            self.url,
            {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
        )

        # Check that the user is redirected and no review is added
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Hospital_Reviews.objects.count(), 0)

    def test_non_patient_user_cannot_add_review(self):
        # Create a non-patient user
        non_patient_user = User.objects.create_user(
            username="non_patient@example.com", password="password"
        )

        # Log in the non-patient user
        self.client.login(username="non_patient@example.com", password="password")

        # Make a POST request to add a review
        response = self.client.post(
            self.url,
            {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
        )

        # Check that the user is redirected and no review is added
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Hospital_Reviews.objects.count(), 0)
