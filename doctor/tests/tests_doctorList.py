from django.test import TestCase
from doctor.models import Doctor


class TestDoctorListView(TestCase):
    def test_doctor_list_view(self):
        print("\nRunning: test for checking doctor list view and pagination")
        # Create 15 doctors for testing pagination
        for i in range(1, 30):
            Doctor.objects.create(
                name=f"Doctor {i}",
                email=f"doctor{i}@example.com",
                phone="987-654-3210",
                sex="Female",
                address=f"Test Address {i}",
                borough="Queens",
                zip=54321,
                primary_speciality=f"Speciality {i}",
                # Add other fields as needed for Doctor model
            )
        response = self.client.get("/doctor/")

        # Check if the view returns a 200 OK status code
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Doctor 1", count=11
        )  # Order by name, there are 11 Doctor 1x

        # Pagination checks
        # Check if a pagination element exists in the HTML
        self.assertContains(response, '<div class="pagination">')
        # Check if there are 2 pagination links (2 pages)
        self.assertContains(response, 'class="page active"', count=1)
        self.assertContains(response, 'class="page"', count=2)

        print("Completed: test for checking doctor list view")

    def test_filter_doctors_by_speciality(self):
        print("\nRunning: test for filtering doctors by speciality")

        # Create doctors with different specialities
        Doctor.objects.create(
            name="Doctor A",
            email="doctorA@example.com",
            phone="987-654-3210",
            sex="Female",
            address="Test Address A",
            borough="Queens",
            zip=54321,
            primary_speciality="Cardiology",
        )

        Doctor.objects.create(
            name="Doctor B",
            email="doctorB@example.com",
            phone="987-654-3210",
            sex="Female",
            address="Test Address B",
            borough="Queens",
            zip=54321,
            primary_speciality="Dermatology",
        )

        Doctor.objects.create(
            name="Doctor C",
            email="doctorC@example.com",
            phone="987-654-3210",
            sex="Female",
            address="Test Address C",
            borough="Queens",
            zip=54321,
            primary_speciality="Cardiology",
        )

        url = "/doctor/"
        url += "?page=1&primary_speciality=Cardiology&borough=All&address=All&zip=All&name="
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Check if only Cardiology doctors are displayed
        self.assertContains(response, "Doctor A")
        self.assertNotContains(response, "Doctor B")
        self.assertContains(response, "Doctor C")

        print("Completed: test for filtering doctors by speciality")

    def test_search_doctors_by_name(self):
        print("\nRunning: test for searching doctors by name")

        # Create doctors with different specialities
        Doctor.objects.create(
            name="Doctor A",
            email="doctorA@example.com",
            phone="987-654-3210",
            sex="Female",
            address="Test Address A",
            borough="Queens",
            zip=54321,
            primary_speciality="Cardiology",
        )

        Doctor.objects.create(
            name="Doctor B",
            email="doctorB@example.com",
            phone="987-654-3210",
            sex="Female",
            address="Test Address B",
            borough="Queens",
            zip=54321,
            primary_speciality="Dermatology",
        )

        url = "/doctor/"
        url += "?page=1&primary_speciality=All&borough=All&address=All&zip=All&name=Doctor A"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # Check if only Cardiology doctors are displayed
        self.assertContains(response, "Doctor A")
        self.assertNotContains(response, "Doctor B")
        self.assertNotContains(response, "Doctor C")

        print("Completed: test for searching doctors by name")

    def test_empty_list(self):
        # Ensure the view works when there are no doctors in the database
        response = self.client.get("/doctor/")
        self.assertEqual(response.status_code, 200)

        # Check if there are no doctors displayed in the response
        self.assertQuerysetEqual(response.context["object_list"], [])

        # Check if the appropriate message for an empty list is present in the response
        self.assertContains(response, "no doctors are available")
