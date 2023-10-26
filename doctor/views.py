from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic
from user.models import User
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Doctor, DoctorAppointment


class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = "doctor/doctor_details.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DoctorListView(generic.ListView):
    template_name = "doctor/doctor_list.html"

    # doctor list object name in html
    context_object_name = "doctor_list"

    def get_queryset(self):
        return Doctor.objects.filter().order_by("name")


@xframe_options_exempt
@csrf_exempt
def book_consultation(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    try:
        body = json.load(request)
        user_id = 1
        start_time = datetime.strptime(
            f'{body["date"]} {body["time"]}', "%Y-%m-%d %H:%M"
        )
        start_time = timezone.make_aware(start_time)
        name = body["name"]
        phone = body["phone"]
        email = body["email"]
        reason = body["reason"]

    except Exception as e:
        print("Error: ", e)
        return HttpResponseBadRequest("Invalid Request")

    else:
        appointment = DoctorAppointment()
        appointment.user = get_object_or_404(User, pk=user_id)
        appointment.doctor = doctor
        appointment.name = name
        appointment.phone = phone
        appointment.email = email
        appointment.reason = reason
        appointment.start_time = start_time
        appointment.status = "REQ"
        appointment.save()
        print("Online Appointment Saved")
        return HttpResponse(
            "Online Consultation Request Created Successfully!", status=200
        )
