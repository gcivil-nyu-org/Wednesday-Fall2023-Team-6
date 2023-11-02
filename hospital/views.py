from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import generic
from .models import Hospital, HospitalAppointment
from user.models import User
from doctor.models import Doctor
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator
from .forms import HospitalFilterForm


class HospitalDetailView(generic.DetailView):
    model = Hospital
    template_name = "hospital/hospital_details.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


def TempDetails(request):
    template_name = "hospital/hospital_details.html"
    return render(request, template_name)


def get_hospitals(request):
    # Query all hospitals from the database
    hospitals = Hospital.objects.all()

    # Convert queryset to a list of dictionaries
    hospital_list = [
        {
            "name": hospital.name,
            "facility_type": hospital.facility_type,
            # Add other fields as needed
        }
        for hospital in hospitals
    ]

    # Return the list as JSON
    return JsonResponse({"hospitals": hospital_list})


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
