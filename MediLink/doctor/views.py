from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views import generic
from django.urls import reverse
from user.models import User
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
import json
from hospital.models import Hospital
from .models import Doctor, DoctorAppointment

class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = 'Doctor/doctor_details.html'

@xframe_options_exempt
@csrf_exempt
def book_consultation(request, doctor_id):
    Doctor = get_object_or_404(Hospital, pk=doctor_id)  
    try:
        body = json.load(request)
        user_id = 1 
        start_time = datetime.strptime(f'{body["date"]} {body["time"]}', '%Y-%m-%d %H:%M')
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
        appointment = DoctorAppointment()
        appointment.user = get_object_or_404(User, pk=user_id)
        appointment.doctor = Doctor
        appointment.name = name
        appointment.phone = phone
        appointment.email = email
        appointment.reason = reason
        appointment.accebility = accebility
        appointment.start_time = start_time
        appointment.preferred_doctor = preferred_doctor
        appointment.status = "REQ"
        appointment.save()
        print("Online Appointment Saved")
        return HttpResponseRedirect(reverse("doctor:detail_view", args=(doctor_id,)))
