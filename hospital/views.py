from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic
from .models import Hospital, HospitalAppointment
from user.models import User
from doctor.models import Doctor
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
import json


class HospitalDetailView(generic.DetailView):
    model = Hospital
    template_name = "hospital/hospital_details.html"


@xframe_options_exempt
@csrf_exempt
def book_appointment(request, hospital_id):
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    try:
        body = json.load(request)
        user_id = 1
        start_time = datetime.strptime(
            f'{body["date"]} {body["time"]}', "%Y-%m-%d %H:%M"
        )
        start_time = timezone.make_aware(start_time)
        preferred_doctor = get_object_or_404(Doctor, pk=1)
        name = body["name"]
        phone = body["phone"]
        email = body["email"]
        reason = body["reason"]
        accebility = body["accebility"]

    except Exception as e:
        print("Error: ", e)
        return HttpResponseBadRequest("Invalid Request")

    else:
        appointment = HospitalAppointment()
        appointment.user = get_object_or_404(User, pk=user_id)
        appointment.hospital = hospital
        appointment.name = name
        appointment.phone = phone
        appointment.email = email
        appointment.reason = reason
        appointment.accebility = accebility
        appointment.start_time = start_time
        appointment.preferred_doctor = preferred_doctor
        appointment.status = "REQ"
        appointment.save()
        print("Appointment Saved")

        return HttpResponse("Appointment Request Created Successfully!", status=200)