from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import generic
from user.models import Choices, Doctor_Reviews, Patient
from django.utils import timezone
import json
from .models import Doctor, DoctorAppointment
from django.core.paginator import Paginator
from .forms import DoctorFilterForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import Avg
from django.contrib import messages


class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = "doctor/doctor_details.html"
    borough_converter = {}

    for borough in Choices.boroughs:
        borough_converter[borough[0]] = borough[1]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get doctor reviews related to the current doctor
        doctor_reviews = Doctor_Reviews.objects.filter(doctor=context["object"])
        if doctor_reviews.aggregate(Avg("rating"))["rating__avg"]:
            average_rating = doctor_reviews.aggregate(Avg("rating"))["rating__avg"]
        else:
            average_rating = 0
        # Add doctor reviews to the context
        context["doctor_reviews"] = doctor_reviews
        context["average_rating"] = average_rating
        try:
            context["object"].borough = self.borough_converter[
                context["object"].borough
            ]
        except Exception as e:
            print("Doctor Borough Exception: ", e)

        return context


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
            #address = filter_form.cleaned_data.get("address")
            borough = filter_form.cleaned_data.get("borough")
            zip = filter_form.cleaned_data.get("zip")

            if name:
                """
                to make the name contains the input name
                """
                doctors = doctors.filter(name__icontains=name)
            if primary_speciality and primary_speciality != "All":
                doctors = doctors.filter(primary_speciality=primary_speciality)
            # if address and address != "All":
            #     doctors = doctors.filter(address=address)
            if borough and borough != "All":
                doctors = doctors.filter(borough=borough)
            if zip and zip != "All":
                doctors = doctors.filter(zip=zip)
            
            ratings = filter_form.cleaned_data.get("ratings")
            try:
                ratings = int(ratings)
                if ratings > 0:
                    doctors = doctors.annotate(avg_rating=Avg('doctor_reviews__rating')).filter(avg_rating__gte=ratings)
            except (TypeError, ValueError):
                # Handle the case where ratings is not a valid number
                pass 
        return doctors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        """
        Pagination use the paginator  to make pagination,
        which contains two variables,
        the first one is the context doctor list from get_queryset,
        the second one is the quantity of the page items.
        """
        paginator = Paginator(context["doctor_list"], 12)
        page_number = self.request.GET.get("page")
        doctor_list = paginator.get_page(page_number)
        context["doctor_list"] = doctor_list

        doctor_reviews = []
        doctor_ratings = []
        for doctor in doctor_list:
            reviews = Doctor_Reviews.objects.filter(doctor=doctor).order_by("-posted")

            if reviews.aggregate(Avg("rating"))["rating__avg"]:
                average_rating = round(float(reviews.aggregate(Avg("rating"))["rating__avg"]))
            else:
                average_rating = 0

            doctor_ratings.append(average_rating)
            if len(reviews):
                doctor_reviews.append(reviews[0].description)
            else:
                doctor_reviews.append("")

        context["doctor_reviews"] = doctor_reviews
        context["doctor_ratings"] = doctor_ratings
        # Get filter parameters from the URL
        primary_speciality = self.request.GET.get("primary_speciality", "all")
        address = self.request.GET.get("address", "all")
        borough = self.request.GET.get("borough", "all")
        zip = self.request.GET.get("zip", "all")
        name = self.request.GET.get("name", "")
        context["filter_form"] = DoctorFilterForm(
            initial={
                "primary_speciality": primary_speciality,
                "address": address,
                "borough": borough,
                "zip": zip,
                "name": name,
            }
        )
        return context


def check_appointment_overlap(patient, appointment_dtime):
    end_time = appointment_dtime + timedelta(minutes=30)

    start_check = Q(start_time__lte=end_time)
    end_check = Q(start_time__gte=(appointment_dtime - timedelta(minutes=30)))
    status_check = Q(status="REQ") | Q(status="CNF")
    overlapping_appointments = DoctorAppointment.objects.filter(
        start_check & end_check & status_check,
        patient=patient,
    )

    if overlapping_appointments.exists():
        return (True, "You have an overlapping appointment/request at that time")
    else:
        return (False, "")


def book_consultation(request, doctor_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseBadRequest(
                "Cannot create an appointment without an account. Please Login!"
            )

        doctor = get_object_or_404(Doctor, pk=doctor_id)
        try:
            body = json.loads(request.body.decode("utf-8"))
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

            name = body["name"]
            phone = body["phone"]
            email = body["email"]
            reason = body["reason"]

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print("Error:", e)
            return HttpResponseBadRequest("Invalid Request")

        try:
            appointment = DoctorAppointment(
                patient=user,
                doctor=doctor,
                name=name,
                phone=phone,
                email=email,
                reason=reason,
                start_time=start_time,
                status="REQ",
            )
            appointment.full_clean()  # Validate model fields
            appointment.save()
            print("Online Appointment Saved")
            return HttpResponse(
                "Online Consultation Request Created Successfully!", status=200
            )

        except ValidationError as ve:
            print("Validation Error:", ve)
            return HttpResponseBadRequest(
                "Validation Error! Please ensure your details are correct"
            )

    return HttpResponseBadRequest("Invalid Request Method")


def add_review(request, doctor_id):
    if request.method == "POST":
        # Checks to ensure only patient can add reviews
        if request.user.is_authenticated:
            user = request.user
            if not Patient.objects.filter(email=user.username).exists():
                messages.error(
                    request,
                    "Error: You need to have a patient account to post reviews!",
                )
            else:
                # Fetch items here from request like:
                patient = Patient.objects.filter(email=user.username).first()
                title = request.POST.get("Title")
                rating = request.POST.get("rating")
                description = request.POST.get("Description")
                doctor = get_object_or_404(Doctor, pk=doctor_id)

                review = Doctor_Reviews()
                review.doctor = doctor
                review.review_from = patient.name
                review.rating = rating
                review.description = description
                review.title = title
                review.posted = datetime.now()
                review.save()
        else:
            messages.error(request, "Error: You need to be logged-in to post reviews!")
    return redirect("doctor:detail_view", pk=doctor_id)