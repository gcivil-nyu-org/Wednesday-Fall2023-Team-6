from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class MapViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.map_url = reverse("googleMaps:map")

    @patch("googleMaps.views.map")
    def test_map_view_with_valid_input(self, mock_geocode):
        print("\nRunning: test for valid map input")
        # Mocking the geocode_address function to return a specific latitude and longitude
        mock_geocode.return_value = (40.7128, -74.0060)

        response = self.client.get(
            self.map_url,
            {
                "name": "Example Hospital",
                "address": "123 Main St",
                "borough": "Manhattan",
                "zip": "10001",
                "type": "Hospital",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "googleMaps/map.html")
        self.assertIn("latitude", response.context)
        self.assertIn("longitude", response.context)
        print("Complete: test for valid map input")

    def test_map_view_with_missing_parameters(self):
        print("\nRunning: test for missing input")
        response = self.client.get(self.map_url)
        self.assertEqual(response.status_code, 400)  # Bad Request
        print("Complete: test for missing input")

    @patch("googleMaps.views.map")
    def test_map_view_with_failed_geocoding(self, mock_geocode):
        print("\nRunning: test for failed geocoding")
        mock_geocode.return_value = (None, None)

        response = self.client.get(
            self.map_url,
            {"address": "xxx", "borough": "xxx", "zip": "x"},
        )

        self.assertEqual(response.status_code, 400)  # Bad Request
        print("\nComplete: test for failed geocoding")
