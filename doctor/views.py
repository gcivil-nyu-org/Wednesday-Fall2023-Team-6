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
from django.core.paginator import Paginator
from .forms import DoctorFilterForm


class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = "doctor/doctor_details.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class DoctorListView(generic.ListView):
    model = Doctor
    template_name = "doctor/doctor_list.html"

    # doctor list object name in html
    context_object_name = "doctor_list"

    def get_queryset(self):
        doctors = Doctor.objects.all().order_by("name")
        filter_form = DoctorFilterForm(self.request.GET)

        """
        filter backend implementation
        """
        if filter_form.is_valid():
            name = filter_form.cleaned_data.get("name")
            primary_speciality = filter_form.cleaned_data.get("primary_speciality")
            address = filter_form.cleaned_data.get("address")
            borough = filter_form.cleaned_data.get("borough")
            zip_code = filter_form.cleaned_data.get("zip")

            if name:
                """
                to make the name contains the input name
                """
                doctors = doctors.filter(name__contains=name)
            if primary_speciality and primary_speciality != "All":
                doctors = doctors.filter(primary_speciality=primary_speciality)
            if address and address != "All":
                doctors = doctors.filter(address=address)
            if borough and borough != "All":
                doctors = doctors.filter(borough=borough)
            if zip_code and zip_code != "All":
                doctors = doctors.filter(zip=zip_code)

        return doctors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """
        Pagination use the paginator to make pagination,
        which contains two variables,
        the first one is the context doctor list from get_queryset,
        the second one is the quantity of the page items.
        """
        paginator = Paginator(context["doctor_list"], 12)
        page_number = self.request.GET.get("page")
        doctor_list = paginator.get_page(page_number)
        context["doctor_list"] = doctor_list

        # Get filter parameters from the URL
        primary_speciality = self.request.GET.get("primary_speciality", "all")
        address = self.request.GET.get("address", "all")
        borough = self.request.GET.get("borough", "all")
        zip = self.request.GET.get("zip_code", "all")
        name = self.request.GET.get("name", "")
        context["filter_form"] = DoctorFilterForm(
            initial={
                "primary_speciality": primary_speciality,
                "address": address,
                "borough": borough,
                "zip_code": zip,
                "name": name,
            }
        )
        return context


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
