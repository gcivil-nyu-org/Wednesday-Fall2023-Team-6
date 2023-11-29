from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from hospital.models import Hospital
from user.models import Patient, Hospital_Reviews
 #  from hospital.views import add_review


class AddReviewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a user with patient role
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

        self.url = reverse("hospital:add_review", args=[self.hospital.id])

    def test_authenticated_user_can_add_review(self):
        # Log in the patient user
        self.client.login(username="testuser@example.com", password="testpassword")

        # Make a POST request to add a review
        response = self.client.post(
            self.url,
            {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
        )

        # Check that the review was added successfully
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Hospital_Reviews.objects.count(), 1)

    def test_unauthenticated_user_cannot_add_review(self):
        # Make a POST request to add a review without logging in
        response = self.client.post(
            self.url,
            {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
        )

        # Check that the user is redirected and no review is added
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(Hospital_Reviews.objects.count(), 0)

    # def test_non_patient_user_cannot_add_review(self):
    #     # Create a non-patient user
    #     non_patient_user = User.objects.create_user(
    #         username="non_patient@example.com", password="password"
    #     )

    #     # Log in the non-patient user
    #     self.client.login(username="non_patient@example.com", password="password")

    #     # Make a POST request to add a review
    #     response = self.client.post(
    #         self.url,
    #         {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
    #     )

    #     # Check that the user is redirected and no review is added
    #     self.assertEqual(response.status_code, 302)  # Redirect status code
    #     self.assertEqual(Hospital_Reviews.objects.count(), 0)
# from django.test import TestCase, Client
# from django.urls import reverse
# from django.contrib.auth.models import User
# from hospital.models import Hospital
# from user.models import Patient, Hospital_Reviews

# # from hospital.views import add_review


# class AddReviewTestCase(TestCase):
#     def setUp(self):
#         self.client = Client()
#         # Create a user with patient role
#         self.user = User.objects.create_user(
#             username="testuser@example.com",
#             password="testpassword",
#             email="testuser@example.com",
#         )

#         self.hospital = Hospital.objects.create(
#             name="Test Hospital",
#             facility_type="Type A",
#             borough="BKN",
#             phone="123-456-7890",
#             location="Location A",
#             postal_code=12345,
#         )

#         self.patient = Patient.objects.create(
#             email="testuser@example.com",
#             name="Test User",
#             phone="1234567890",
#             address="123 Street",
#             borough="Borough",
#             zip="54321",
#         )

#         self.url = reverse("hospital:add_review", args=[self.hospital.id])

#     def test_authenticated_user_can_add_review(self):
#         # Log in the patient user
#         self.client.login(username="testuser@example.com", password="testpassword")

#         # Make a POST request to add a review
#         response = self.client.post(
#             self.url,
#             {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
#         )
#         response = self.client.post(
#             self.url,
#             {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
#         )

#         # Check that the review was added successfully
#         self.assertEqual(response.status_code, 302)  # Redirect status code
#         self.assertEqual(Hospital_Reviews.objects.count(), 1)

#     def test_unauthenticated_user_cannot_add_review(self):
#         # Make a POST request to add a review without logging in
#         response = self.client.post(
#             self.url,
#             {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
#         )
#         response = self.client.post(
#             self.url,
#             {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
#         )

#         # Check that the user is redirected and no review is added
#         self.assertEqual(response.status_code, 302)  # Redirect status code
#         self.assertEqual(Hospital_Reviews.objects.count(), 0)

#     # def test_non_patient_user_cannot_add_review(self):
#     #     # Create a non-patient user
#     #     non_patient_user = User.objects.create_user(
#     #         username="non_patient@example.com", password="password"
#     #     )

#     #     # Log in the non-patient user
#     #     self.client.login(username="non_patient@example.com", password="password")

#     #     # Make a POST request to add a review
#     #     response = self.client.post(
#     #         self.url,
#     #         {"Title": "Test Review", "rating": 4, "Description": "Test Description"},
#     #     )

#     #     # Check that the user is redirected and no review is added
#     #     self.assertEqual(response.status_code, 302)  # Redirect status code
#     #     self.assertEqual(Hospital_Reviews.objects.count(), 0)
