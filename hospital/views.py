from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic
from .models import Hospital, HospitalAppointment
from user.models import Patient
from doctor.models import Doctor
from django.utils import timezone
import json
from django.core.paginator import Paginator
from .forms import HospitalFilterForm
from django.db.models import Q


class HospitalDetailView(generic.DetailView):
    model = Hospital
    template_name = "hospital/hospital_details.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(HospitalDetailView, self).get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all().filter(
            associated_hospital=context["object"]
        )
        return context


class HospitalListView(generic.ListView):
    model = Hospital
    template_name = "hospital/hospital_list.html"

    # doctor list object name in html
    context_object_name = "hospital_list"

    def get_queryset(self):
        hospitals = Hospital.objects.all().order_by("name")
        filter_form = HospitalFilterForm(self.request.GET)

        """
        filter backend implementation
        """
        if filter_form.is_valid():
            name = filter_form.cleaned_data.get("name")
            facility_type = filter_form.cleaned_data.get("facility_type")
            location = filter_form.cleaned_data.get("location")
            borough = filter_form.cleaned_data.get("borough")
            postal_code = filter_form.cleaned_data.get("postal_code")

            if name:
                """
                to make the name contains the input name
                """
                hospitals = hospitals.filter(name__contains=name)
            if facility_type and facility_type != "All":
                hospitals = hospitals.filter(facility_type=facility_type)
            if location and location != "All":
                hospitals = hospitals.filter(location=location)
            if borough and borough != "All":
                hospitals = hospitals.filter(borough=borough)
            if postal_code and postal_code != "All":
                hospitals = hospitals.filter(postal_code=postal_code)

        return hospitals

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """
        Pagination use the paginator to make pagination,
        which contains two variables,
        the first one is the context hospital list from get_queryset,
        the second one is the quantity of the page items.
        """
        paginator = Paginator(context["hospital_list"], 12)
        page_number = self.request.GET.get("page")
        hospital_list = paginator.get_page(page_number)
        context["hospital_list"] = hospital_list

        # Get filter parameters from the URL
        facility_type = self.request.GET.get("facility_type", "all")
        location = self.request.GET.get("location", "all")
        borough = self.request.GET.get("borough", "all")
        postal_code = self.request.GET.get("postal_code", "all")
        name = self.request.GET.get("name", "")
        context["filter_form"] = HospitalFilterForm(
            initial={
                "facility_type": facility_type,
                "location": location,
                "borough": borough,
                "postal_code": postal_code,
                "name": name,
            }
        )
        return context


def check_appointment_overlap(patient, appointment_dtime):
    end_time = appointment_dtime + timedelta(minutes=30)

    start_check = Q(start_time__lte=end_time)
    end_check = Q(start_time__gte=(appointment_dtime - timedelta(minutes=30)))
    overlapping_appointments = HospitalAppointment.objects.filter(
        start_check & end_check,
        patient=patient,
    )

    if overlapping_appointments.exists():
        return (True, "You have an overlapping appointment/request at that time")
    else:
        return (False, "")


def book_appointment(request, hospital_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseBadRequest(
                "Cannot create an appointment without an account. Please Login!"
            )

        hospital = get_object_or_404(Hospital, pk=hospital_id)
        try:
            body = json.load(request)
            if Patient.objects.all().filter(email=request.user.username).exists():
                user = get_object_or_404(Patient, email=request.user.username)
            else:
                return HttpResponseBadRequest(
                    "You need to have a Patient account to create appointments!"
                )

            start_time = datetime.strptime(
                f'{body["date"]} {body["time"]}', "%Y-%m-%d %H:%M"
            )
            start_time = timezone.make_aware(start_time)

            overlap, overlap_message = check_appointment_overlap(user, start_time)
            if overlap:
                return HttpResponseBadRequest(overlap_message)

            preferred_doctor = None
            print(body["preferred_doctor"])
            if body["preferred_doctor"]:
                preferred_doctor = get_object_or_404(
                    Doctor, pk=int(body["preferred_doctor"])
                )

            name = body["name"]
            phone = body["phone"]
            email = body["email"]
            reason = body["reason"]
            accebility = body["accebility"]

        except Exception as e:
            print("Error: ", e)
            return HttpResponseBadRequest("Invalid Request")

        try:
            appointment = HospitalAppointment()
            appointment.patient = user
            appointment.hospital = hospital
            appointment.name = name
            appointment.phone = phone
            appointment.email = email
            appointment.reason = reason
            appointment.accebility = accebility
            appointment.start_time = start_time
            appointment.preferred_doctor = preferred_doctor
            appointment.status = "REQ"

            appointment.full_clean()
            appointment.save()
            print("Appointment Saved")
            return HttpResponse("Appointment Request Created Successfully!", status=200)
        except ValidationError as ve:
            print("Validation Error:", ve)
            return HttpResponseBadRequest(
                "Validation Error! Please ensure your details are correct"
            )

    return HttpResponseBadRequest("Invalid Request Method")
