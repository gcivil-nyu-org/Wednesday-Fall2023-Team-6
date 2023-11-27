from django.test import TestCase
from django.urls import reverse
from user.models import Doctor_Reviews, Hospital_Reviews
from doctor.models import Doctor
from hospital.models import Hospital


class ReviewsSectionTest(TestCase):
    def setUp(self):
        # Create a sample doctor
        self.doctor = Doctor.objects.create(
            email="doctor@example.com",
            name="Dr. Sample",
            phone="1234567890",
            address="123 Medical Street",
            borough="MHT",
            zip="54321",
            primary_speciality="General Medicine",
            active_status=True,
        )

        # Create a sample hospital
        self.hospital = Hospital.objects.create(
            name="Sample Hospital",
            facility_type="General",
            borough="MHT",
            phone="1112223333",
            location="789 Hospital Street",
            postal_code=67890,
            latitude=40.7128,
            longitude=-74.0060,
        )

        # Create sample reviews for the doctor
        Doctor_Reviews.objects.create(
            likes="Positive Review",
            review_from="Patient 1",
            rating=5,
            description="This doctor is amazing!",
            doctor=self.doctor,
        )
        Doctor_Reviews.objects.create(
            likes="Negative Review",
            review_from="Patient 2",
            rating=2,
            description="Not satisfied with the service.",
            doctor=self.doctor,
        )

        # Create sample reviews for the hospital
        Hospital_Reviews.objects.create(
            likes="Positive Review",
            review_from="Patient 3",
            rating=4,
            description="Great hospital experience!",
            hospital=self.hospital,
        )
        Hospital_Reviews.objects.create(
            likes="Neutral Review",
            review_from="Patient 4",
            rating=3,
            description="Average service.",
            hospital=self.hospital,
        )

    def test_doctor_reviews_rendering(self):
        response = self.client.get(
            reverse("home")
        )  # Replace 'home' with the actual URL name
        self.assertContains(response, "Doctor Reviews")
        self.assertContains(response, "Positive Review")
        self.assertContains(response, "Negative Review")
        self.assertContains(response, "This doctor is amazing!")
        self.assertContains(response, "Not satisfied with the service.")

    def test_hospital_reviews_rendering(self):
        response = self.client.get(
            reverse("home")
        )  # Replace 'home' with the actual URL name
        self.assertContains(response, "Hospital Reviews")
        self.assertContains(response, "Positive Review")
        self.assertContains(response, "Neutral Review")
        self.assertContains(response, "Great hospital experience!")
        self.assertContains(response, "Average service.")

    def tearDown(self):
        self.doctor.delete()
        self.hospital.delete()
        Doctor_Reviews.objects.all().delete()
        Hospital_Reviews.objects.all().delete()
