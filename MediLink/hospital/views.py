from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Hospital, HospitalAppointment
from user.models import User

class HospitalDetailView(generic.DetailView):
    model = Hospital
    template_name = 'hospital/hospital_detail.html'

def book_appointment(request, hospital_id):
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    
    try:
        user_id = ""
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        preferred_doctor = request.POST['preferred_doctor']
        
    except:
        return render(request, 'hospital/hospital_detail.html', {
            'hospital': hospital,
            'error_message': "Invalid details! Please ensure all the appointment details are valid!",
        })
    
    else:
        appointment = HospitalAppointment()
        appointment.user = get_object_or_404(User, pk=user_id)
        appointment.hospital = hospital
        appointment.start_time = start_time
        appointment.end_time = end_time
        appointment.preferred_doctor = preferred_doctor
        appointment.assigned_doctor = None
        appointment.status = "REQ"
    
    return HttpResponseRedirect(reverse('hospital:detail_view', args=(hospital_id,)))
