from django.test import TestCase
from django.urls import reverse
from hospital.models import Hospital


class HospitalListViewTest(TestCase):
    def test_hospital_filtering_name(self):
        print("\nRunning: test for filtering hospitals by name")

        # Create a test Hospital
        Hospital.objects.create(
            name="Hospital A",
            facility_type="Type A",
            borough="BKN",
            phone="123-456-7890",
            location="Location A",
            postal_code=12345,
        )

        Hospital.objects.create(
            name="Hospital B",
            facility_type="Type B",
            borough="QNS",
            phone="576-293-4829",
            location="Location B",
            postal_code=54321,
        )

        url = "/hospital/"
        url += "?page=1&facility_type=All&borough=All&location=All&postal_code=All&name=Hospital A"

        # Perform a search of name
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Check if only borough doctors are displayed
        self.assertNotContains(response, "Hospital B")
        self.assertContains(response, "Hospital A")

        print("Completed: test for filtering hospitals by name")

    def test_hospital_filtering_facility(self):
        print("\nRunning: test for filtering hospitals by facility type")

        # Create a test Hospital
        Hospital.objects.create(
            name="Hospital A",
            facility_type="Type A",
            borough="BKN",
            phone="123-456-7890",
            location="Location A",
            postal_code=12345,
        )

        Hospital.objects.create(
            name="Hospital B",
            facility_type="Type B",
            borough="QNS",
            phone="576-293-4829",
            location="Location B",
            postal_code=54321,
        )

        url = "/hospital/"
        url += "?page=1&facility_type=Type A&borough=All&location=All&postal_code=All&name="

        # Perform a search of name
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Check if only borough doctors are displayed
        self.assertNotContains(response, "Hospital B")
        self.assertContains(response, "Hospital A")

        print("Completed: test for filtering hospitals by facility type")

    def test_hospital_filtering_borough(self):
        print("\nRunning: test for filtering hospitals by borough")

        # Create a test Hospital
        Hospital.objects.create(
            name="Hospital A",
            facility_type="Type A",
            borough="BKN",
            phone="123-456-7890",
            location="Location A",
            postal_code=12345,
        )

        Hospital.objects.create(
            name="Hospital B",
            facility_type="Type B",
            borough="QNS",
            phone="576-293-4829",
            location="Location B",
            postal_code=54321,
        )

        url = "/hospital/"
        url += (
            "?page=1&facility_type=All&borough=BKN&location=All&postal_code=All&name="
        )

        # Perform a search of name
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Check if only borough doctors are displayed
        self.assertNotContains(response, "Hospital B")
        self.assertContains(response, "Hospital A")

        print("Completed: test for filtering hospitals by borough")

    # def test_hospital_filtering_location(self):
    #     print("\nRunning: test for filtering hospitals by location")

    #     # Create a test Hospital
    #     Hospital.objects.create(
    #         name="Hospital A",
    #         facility_type="Type A",
    #         borough="BKN",
    #         phone="123-456-7890",
    #         location="Location A",
    #         postal_code=12345,
    #     )

    #     Hospital.objects.create(
    #         name="Hospital B",
    #         facility_type="Type B",
    #         borough="QNS",
    #         phone="576-293-4829",
    #         location="Location B",
    #         postal_code=54321,
    #     )

    #     url = "/hospital/"
    #     url += "?page=1&facility_type=All&borough=All&location=Location A&postal_code=All&name="

    #     # Perform a search of name
    #     response = self.client.get(url)

    #     self.assertEqual(response.status_code, 200)
    #     # Check if only borough doctors are displayed
    #     self.assertNotContains(response, "Hospital B")
    #     self.assertContains(response, "Hospital A")

    #     print("Completed: test for filtering hospitals by location")

    def test_hospital_filtering_postal(self):
        print("\nRunning: test for filtering hospitals by postal code")

        # Create a test Hospital
        Hospital.objects.create(
            name="Hospital A",
            facility_type="Type A",
            borough="BKN",
            phone="123-456-7890",
            location="Location A",
            postal_code=12345,
        )

        Hospital.objects.create(
            name="Hospital B",
            facility_type="Type B",
            borough="QNS",
            phone="576-293-4829",
            location="Location B",
            postal_code=54321,
        )

        url = "/hospital/"
        url += (
            "?page=1&facility_type=All&borough=All&location=All&postal_code=12345&name="
        )

        # Perform a search of name
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        # Check if only borough doctors are displayed
        self.assertNotContains(response, "Hospital B")
        self.assertContains(response, "Hospital A")

        print("Completed: test for filtering hospitals by postal code")


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
