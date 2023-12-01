from django.shortcuts import render
from django.http import HttpResponseBadRequest
import requests


def map(request):
    template_name = "googleMaps/map.html"

    name = request.GET.get("name")
    address = request.GET.get("address")
    borough = request.GET.get("borough")
    state = "NY"
    zip_code = request.GET.get("zip")
    type = request.GET.get("type")

    if address and borough and zip_code:
        full_address = f"{address}, {borough}, {state} {zip_code}"
        lat, lon = geocode_address(full_address)

        if lat is None or lon is None:
            return HttpResponseBadRequest("Geocoding failed.")

        return render(
            request,
            template_name,
            {
                "type": type,
                "latitude": lat,
                "longitude": lon,
                "name": name,
                "address": address,
                "borough": borough,
                "state": state,
                "zip_code": zip_code,
            },
        )

    else:
        return HttpResponseBadRequest("Invalid access. Parameters are missing.")


def geocode_address(address):
    api_key = "AIzaSyC5D37u8CYmG2wOkDJniUIBO-OBWXvCgbI"
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None
