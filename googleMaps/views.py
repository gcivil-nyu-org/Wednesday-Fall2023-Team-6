from django.shortcuts import render


# Create your views here.
def doctor_map(request):
    template_name = "googleMaps/doctorMap.html"
    lat, lon = 40.7167, -74.0000
    return render(request, template_name, {"latitude": lat, "longitude": lon})
