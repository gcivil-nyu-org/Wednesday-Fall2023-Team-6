from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from user.models import Patient, Hospital_Reviews
from hospital.models import Hospital


class AddHospitalReviewTestCase(TestCase):
    def setUp(self):
        # Create a user
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

        self.patient = Patient.objects.create(
            email="testuser@example.com",
            name="Test User",
            phone="1234567890",
            address="123 Street",
            borough="Borough",
            zip="54321",
        )

    def test_add_hospital_review_authenticated_patient(self):
        print("\nRunning: test for adding hospital review by authenticated patient")

        # Log in the user
        self.client.force_login(self.user)

        # Post data to add hospital review
        response = self.client.post(
            reverse("hospital:add_review", args=[self.hospital.id]),
            {
                "Title": "Test Review",
                "rating": 5,
                "Description": "This is a test review.",
            },
        )

        # Check if the review is added successfully
        self.assertEqual(
            response.status_code, 302
        )  # 302 indicates a successful redirect
        self.assertEqual(Hospital_Reviews.objects.count(), 1)

        print("\nCompleted: test for adding hospital review by authenticated patient")

    # def test_add_hospital_review_unauthenticated_user(self):
    #     print("\nRunning: test for adding hospital review by unauthenticated user")

    #     # Try to add a review without logging in
    #     response = self.client.post(reverse('add_review', args=[self.hospital.id]), {
    #         'Title': 'Test Review',
    #         'rating': 5,
    #         'Description': 'This is a test review.'
    #     })

    #     # Check if the user is redirected to the login page
    #     self.assertEqual(response.status_code, 302)  # 302 indicates a successful redirect
    #     self.assertRedirects(response, f'/accounts/login/?next={reverse("add_review", args=[self.hospital.id])}')

    #     # Check that no review is added
    #     self.assertEqual(Hospital_Reviews.objects.count(), 0)

    #     print("\nCompleted: test for adding hospital review by unauthenticated user")

    # def test_add_hospital_review_non_patient_user(self):
    #     print("\nRunning: test for adding hospital review by non-patient user")

    #     # Create a user who is not a patient
    #     user = User.objects.create_user(username='nonpatient', password='testpassword')

    #     # Log in the non-patient user
    #     self.client.force_login(user)

    #     # Try to add a review
    #     response = self.client.post(reverse('add_review', args=[self.hospital.id]), {
    #         'Title': 'Test Review',
    #         'rating': 5,
    #         'Description': 'This is a test review.'
    #     })

    #     # Check if the user receives an error message
    #     self.assertEqual(response.status_code, 200)  # 200 indicates a successful response
    #     self.assertContains(response, 'You need to have a patient account to post reviews!')

    #     # Check that no review is added
    #     self.assertEqual(Hospital_Reviews.objects.count(), 0)

    #     print("\nCompleted: test for adding hospital review by non-patient user")
