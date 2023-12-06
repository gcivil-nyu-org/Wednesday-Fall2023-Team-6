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
        positive_review_doctor = Doctor_Reviews.objects.create(
            title="Positive Review",
            review_from="Patient 1",
            rating=5,
            description="This doctor is amazing!",
        )
        negative_review_doctor = Doctor_Reviews.objects.create(
            title="Negative Review",
            review_from="Patient 2",
            rating=2,
            description="Not satisfied with the service.",
        )
        positive_review_doctor.doctor.add(self.doctor)
        negative_review_doctor.doctor.add(self.doctor)

        # Create sample reviews for the hospital
        positive_review_hospital = Hospital_Reviews.objects.create(
            title="Positive Review",
            review_from="Patient 3",
            rating=4,
            description="Great hospital experience!",
        )
        neutral_review_hospital = Hospital_Reviews.objects.create(
            title="Neutral Review",
            review_from="Patient 4",
            rating=3,
            description="Average service.",
        )
        positive_review_hospital.hospital.add(self.hospital)
        neutral_review_hospital.hospital.add(self.hospital)

    def test_doctor_reviews_rendering(self):
        response = self.client.get(reverse("user:home"))
        self.assertContains(response, "Doctor Reviews")
        self.assertContains(response, "Positive Review")
        self.assertContains(response, "Negative Review")
        self.assertContains(response, "This doctor is amazing!")
        self.assertContains(response, "Not satisfied with the service.")

    def test_hospital_reviews_rendering(self):
        response = self.client.get(reverse("user:home"))
        self.assertContains(response, "Hospital Reviews")
        self.assertContains(response, "Positive Review")
        self.assertContains(response, "Neutral Review")
        self.assertContains(response, "Great hospital experience!")
        self.assertContains(response, "Average service.")

    def tearDown(self):
        positive_review_doctor = Doctor_Reviews.objects.get(title="Positive Review")
        negative_review_doctor = Doctor_Reviews.objects.get(title="Negative Review")
        positive_review_hospital = Hospital_Reviews.objects.get(title="Positive Review")
        neutral_review_hospital = Hospital_Reviews.objects.get(title="Neutral Review")

        positive_review_doctor.delete()
        negative_review_doctor.delete()
        positive_review_hospital.delete()
        neutral_review_hospital.delete()
        self.doctor.delete()
        self.hospital.delete()
