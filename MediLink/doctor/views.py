from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Doctor, DoctorAppointment
from user.models import User
from hospital.models import Hospital

class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = 'doctor/doctor_detail.html'

def book_consultation(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    
    try:
        user_id = 1  # Replace with the actual authenticated user ID
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        
    except Exception as e:
        print(e)
        return render(request, 'doctor/doctor_detail.html', {
            'doctor': doctor,
            'error_message': "Invalid details! Please ensure all the consultation details are valid!",
        })
    
    else:
        consultation = DoctorAppointment()
        consultation.user = get_object_or_404(User, pk=user_id)
        consultation.doctor = doctor
        consultation.start_time = start_time
        consultation.end_time = end_time
        consultation.status = "REQ"
        consultation.save()
        print("Consultation Saved")
    
    return HttpResponseRedirect(reverse('doctor:detail_view', args=(doctor_id,)))
