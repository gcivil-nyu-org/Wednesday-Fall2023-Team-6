import io
import re
from datetime import timedelta
import uuid
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from user.models import Choices, Patient
from doctor.models import Doctor, DoctorAppointment
from hospital.models import HospitalAdmin, Hospital, HospitalAppointment
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

# import for email sending
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import logout
from .models import Doctor_Reviews, Hospital_Reviews


# import for avatar changing
import os
from django.conf import settings

# import for checking appointment status
from django.utils import timezone

PASSWORD_RESET_SUBJECT = "MediLink Account Password Reset Request"
DOCTOR_REJECT_SUBJECT = "MediLink Hospital Association Request Rejected"


def logoutView(request):
    logout(request)
    return redirect("user:home")  # Redirect to the login page after logout


def loginView(request):
    if request.method == "POST":
        username = request.POST.get("user_email")
        password = request.POST.get("user_pwd")

        # print(username,password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Login successful")
            return redirect("user:home")  # Redirect to the home page after login

        else:
            messages.error(request, "Incorrect Credentials! User does not exist!")
            return redirect("user:login")
    template_name = "user/login.html"
    return render(request, template_name)


def passwordResetView(request):
    template_name = "user/resetPassword/password_reset.html"

    if request.method == "GET":
        return render(request, template_name)

    else:
        user_email = request.POST.get("user_email")
        if send_email(
            request,
            user_email,
            "user/resetPassword/template_reset_password.html",
            PASSWORD_RESET_SUBJECT,
        ):
            alert_message = "Email sent. Please follow the link to reset your password."
            messages.success(request, alert_message)
            return HttpResponseRedirect(reverse("user:login"))
        else:
            alert_message = (
                "Email not exists in our database. Please register a new account."
            )
            messages.error(request, alert_message)
            return HttpResponseRedirect(reverse("user:user_registration"))


def passwordResetConfirmView(request, uidb64, token):
    template_name = "user/resetPassword/password_reset_confirm.html"
    if request.method == "GET":
        return render(request, template_name, {"uidb64": uidb64, "token": token})

    else:
        try:
            user_email = urlsafe_base64_decode(uidb64).decode("utf-8")
            new_password = request.POST.get("password")
            if not isValidPassword(new_password):
                raise Exception("Invalid Password")
            token_generator = PasswordResetTokenGenerator()
        except Exception as e:
            print(e)
            messages.error(request, "Invalid Details")
            return HttpResponseRedirect(reverse("user:passwordReset"))

        """
            verifying uid64
        """
        if User.objects.filter(username=user_email).exists():
            user = User.objects.get(username=user_email)
            """
                verifying token
            """
            if token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                alert_message = "Password reset successfully, please login."
                messages.success(request, alert_message)
                return HttpResponseRedirect(reverse("user:login"))
            else:
                alert_message = "Token invalid!"
                messages.error(request, alert_message)
                return HttpResponseRedirect(reverse("user:passwordReset"))

        else:
            alert_message = (
                "Some error exists when resetting your password, please try again."
            )
            messages.error(request, alert_message)
            return HttpResponseRedirect(reverse("user:passwordReset"))


def home(request):
    user_borough = None

    if request.user.is_authenticated:
        # Assuming that the user's borough is stored in the User model
        # Adjust this according to your actual model structure
        try:
            user_borough = request.user.borough
        except AttributeError:
            # Handle the case where the borough attribute is not found
            pass

    if user_borough:
        # Filter doctor reviews for the user's borough
        doctor_reviews = Doctor_Reviews.objects.filter(
            doctor_name__icontains=user_borough
        )

        # Filter hospital reviews for the user's borough
        hospital_reviews = Hospital_Reviews.objects.filter(borough=user_borough)
    else:
        # If user is not logged in, fetch all reviews without filtering by borough
        doctor_reviews = Doctor_Reviews.objects.all()
        hospital_reviews = Hospital_Reviews.objects.all()

    return render(
        request,
        "user/home.html",
        {
            "user_borough": user_borough,
            "doctor_reviews": doctor_reviews,
            "hospital_reviews": hospital_reviews,
        },
    )


def accountView(request):  # noqa: C901
    template_name = "user/account.html"
    """
    check weather a user is logged in
    for the account view
    """
    if request.user.is_authenticated:
        user = request.user
        if user.username != "admin":
            patient = Patient.objects.filter(email=user.username)
            doctor = Doctor.objects.filter(email=user.username)
            hospital_admin = HospitalAdmin.objects.filter(email=user.username)

            # check user types
            if len(patient) != 0:
                login_user = patient.first()
                userType = "patient"
                doctor_appointments = DoctorAppointment.objects.filter(
                    patient=login_user
                )
                hospital_appointments = HospitalAppointment.objects.filter(
                    patient=login_user
                )
                requests = None
            elif len(doctor) != 0:
                login_user = doctor.first()
                userType = "doctor"
                doctor_appointments = DoctorAppointment.objects.filter(
                    doctor=login_user
                )
                hospital_appointments = HospitalAppointment.objects.filter(
                    preferred_doctor=login_user
                )
                requests = None
            elif len(hospital_admin) != 0:
                login_user = hospital_admin.first()
                userType = "hospitalAdmin"
                doctor_appointments = None
                hospital_appointments = HospitalAppointment.objects.filter(
                    hospital=login_user.associated_hospital
                )

                if login_user.active_status:
                    hospital_query = Q(
                        associated_hospital=login_user.associated_hospital
                    )
                    status_query = Q(active_status=False)
                    requests = Doctor.objects.filter(hospital_query & status_query)
                else:
                    requests = []

            # check and update the outdated appointments
            OutdatedAppointments(doctor_appointments, hospital_appointments)

            """
                1. Get method
                2. Post method
                    - edit profile
                    - upload avatar
            """
            if request.method == "GET":
                return render(
                    request,
                    template_name,
                    {
                        "login_user": login_user,
                        "userType": userType,
                        "doctor_appointments": doctor_appointments,
                        "hospital_appointments": hospital_appointments,
                        "requests": requests,
                    },
                )
            else:
                # -------------- Upload Avatar --------------
                if len(request.FILES) > 0:
                    IMG_SIZE = 500
                    uploaded_file = request.FILES["avatar"]
                    img = Image.open(uploaded_file)
                    w, h = img.size

                    if w > h:
                        resize_width = IMG_SIZE
                        resize_height = int((h / w) * IMG_SIZE)
                    else:
                        resize_height = IMG_SIZE
                        resize_width = int((w / h) * IMG_SIZE)

                    img = img.resize((resize_width, resize_height))

                    profile_pic = Image.new("RGB", (IMG_SIZE, IMG_SIZE), "white")
                    x_offset = (IMG_SIZE - resize_width) // 2
                    y_offset = (IMG_SIZE - resize_height) // 2
                    profile_pic.paste(img, (x_offset, y_offset))

                    output_image_stream = io.BytesIO()
                    profile_pic.save(output_image_stream, format="JPEG")

                    # Create an InMemoryUploadedFile from the BytesIO object
                    image_name = f"{uuid.uuid4().hex}.jpg"
                    file_path = os.path.join(settings.MEDIA_ROOT, "avatars", image_name)
                    avatar_image = InMemoryUploadedFile(
                        output_image_stream,
                        None,
                        file_path,
                        "image/jpeg",
                        output_image_stream.tell(),
                        None,
                    )

                    if login_user.avatar and "default" not in login_user.avatar.url:
                        try:
                            os.remove(login_user.avatar.path)
                        except Exception as e:
                            print("Could not delete profile picture", e)

                    login_user.avatar.save(image_name, avatar_image)
                    profile_pic.save(file_path)

                    return redirect("user:account")

                # -------------- Edit Account Info --------------
                else:
                    name = request.POST.get("name")
                    phone = request.POST.get("phone")
                    sex = request.POST.get("sex")
                    insurance_provider = request.POST.get("insurance")
                    address = request.POST.get("address")
                    borough = request.POST.get("borough")
                    zip = request.POST.get("zip")
                    specialization = request.POST.get("specialization")
                    associated_hospital = request.POST.get("hospital")
                    hos_name = request.POST.get("associatedHospital")

                    if userType != "patient":
                        if str(hos_name).strip() == "":
                            associated_hospital = None
                        elif not Hospital.objects.filter(name=hos_name).exists():
                            associated_hospital = (
                                login_user.associated_hospital.id
                                if login_user.associated_hospital
                                else None
                            )

                    form_data = {
                        "name": name,
                        "email": login_user.email,
                        "phone": phone,
                        "sex": sex,
                        "user_type": userType
                        if userType != "hospitalAdmin"
                        else "hospital-admin",
                        "primary_speciality": specialization,
                        "associated_hospital": associated_hospital,
                        "insurance_provider": insurance_provider,
                        "address": address,
                        "borough": borough,
                        "zip": zip,
                    }

                    ret, msg = check_user_validity(form_data)

                    if ret:
                        if userType == "doctor":
                            valid_fields = {
                                field.name for field in Doctor._meta.get_fields()
                            }
                        elif userType == "patient":
                            valid_fields = {
                                field.name for field in Patient._meta.get_fields()
                            }
                        elif userType == "hospitalAdmin":
                            valid_fields = {
                                field.name for field in HospitalAdmin._meta.get_fields()
                            }

                        filtered_form = {
                            k: v for k, v in form_data.items() if k in valid_fields
                        }
                        filtered_form["active_status"] = True

                        if userType == "doctor" or userType == "hospitalAdmin":
                            curr_hos = filtered_form["associated_hospital"]
                            prev_hos = login_user.associated_hospital
                            if curr_hos:
                                if curr_hos != prev_hos:
                                    filtered_form["active_status"] = False
                                else:
                                    filtered_form[
                                        "active_status"
                                    ] = login_user.active_status

                        try:
                            for field, value in filtered_form.items():
                                setattr(login_user, field, value)
                            login_user.full_clean()
                            login_user.save()
                        except Exception as e:
                            print(e)
                            messages.error(request, "Error: Invalid Data")
                    else:
                        messages.error(request, msg)

                    return redirect("user:account")

        # admin user logged in, redirect to admin page
        else:
            return HttpResponseRedirect(reverse("admin:index"))

    # visitors should log in to view the account
    # redirect to login page
    else:
        alert_message = "Please login/register to view your account!"
        messages.error(request, alert_message)
        # auto redirect to login page
        return HttpResponseRedirect(reverse("user:login"))


def OutdatedAppointments(doctor_appointments, hospital_appointments):
    now = timezone.now()
    end_time = timedelta(minutes=30)
    # check consultations
    if doctor_appointments:
        for appointment in doctor_appointments:
            if appointment.status == "REQ" and appointment.start_time + end_time < now:
                appointment.status = "CCL"
                appointment.cancel_msg = "Consultation outdated, please book a new one."
                appointment.save()
    # check appointments
    if hospital_appointments:
        for appointment in hospital_appointments:
            if appointment.status == "REQ" and appointment.start_time + end_time < now:
                appointment.status = "CCL"
                appointment.cancel_msg = "Appointment outdated, please book a new one."
                appointment.save()


def cancelAppointment(request):
    appointment_id = request.POST.get("appointment_id")
    appointment_type = request.POST.get("appointment_type")
    operation = request.POST.get("operation")
    cancel_reason = request.POST.get("cancel_reason")

    if appointment_type == "consultation":
        consultation = DoctorAppointment.objects.filter(id=appointment_id).first()
        if consultation.status != "CCL" and consultation.status != "REJ":
            consultation.cancel_msg = cancel_reason
            consultation.status = operation
            consultation.save()
    else:
        appointment = HospitalAppointment.objects.filter(id=appointment_id).first()
        if appointment.status != "CCL" and appointment.status != "REJ":
            appointment.cancel_msg = cancel_reason
            appointment.status = operation
            appointment.save()

    return redirect("user:account")


def check_consultation_overlap(doctor, appointment_dtime):
    end_time = appointment_dtime + timedelta(minutes=30)

    start_check = Q(start_time__lte=end_time)
    end_check = Q(start_time__gte=(appointment_dtime - timedelta(minutes=30)))
    overlapping_appointments = DoctorAppointment.objects.filter(
        start_check & end_check, doctor=doctor, status="CNF"
    )

    if overlapping_appointments.exists():
        return True
    else:
        return False


def confirmAppointment(request):
    appointment_id = request.POST.get("appointment_id")
    appointment_type = request.POST.get("appointment_type")
    operation = request.POST.get("operation")

    if appointment_type == "consultation":
        consultation = DoctorAppointment.objects.filter(id=appointment_id).first()
        if check_consultation_overlap(consultation.doctor, consultation.start_time):
            messages.error(
                "Error: You have an overlapping appointment during that time."
            )
        else:
            consultation.status = operation
            consultation.save()
    else:
        appointment = HospitalAppointment.objects.filter(id=appointment_id).first()
        appointment.status = operation
        appointment.save()
    return redirect("user:account")


def isValidEmail(email):
    if not email:
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True


def isValidPassword(password):
    if not password:
        return False
    if not len(password) >= 8:
        return False
    return True


def check_user_validity(form_data):  # noqa: C901
    try:
        if not form_data["name"]:
            return False, "Error: Invalid Name"
        if not isValidEmail(form_data["email"]):
            return False, "Error: Invalid Email"
        if not form_data["phone"]:
            return False, "Error: Invalid Phone"
        if form_data["sex"] not in [opt[0] for opt in Choices.sex]:
            return False, "Error: Invalid Sex"
        if form_data["user_type"] not in ["patient", "doctor", "hospital-admin"]:
            return False, "Error: Invalid User Type"
        if not form_data["address"]:
            return False, "Invalid Address"
        if not form_data["zip"]:
            return False, "Invalid Zip"
        if form_data["borough"] not in [opt[0] for opt in Choices.boroughs]:
            return False, "Error: Invalid Borough"

        # Conditionally set fields based on user type
        if form_data["user_type"] not in ["doctor", "hospital-admin"]:
            form_data["associated_hospital"] = None
        elif form_data["user_type"] == "doctor" and (
            not form_data["associated_hospital"]
        ):
            form_data["associated_hospital"] = None
        else:
            try:
                form_data["associated_hospital"] = Hospital.objects.get(
                    id=int(form_data["associated_hospital"])
                )
            except Exception as e:
                print("Error: ", e)
                return False, "Error: Invalid Hospital selected."
        if form_data["user_type"] != "patient":
            form_data["insurance_provider"] = None

        return True, ""

    except Exception as e:
        print(e)
        return False, "Invalid User Details"


def get_form_data(request):  # noqa: C901
    # Collecting data from the form
    name = request.POST.get("user_name") or None
    email = request.POST.get("user_email") or None
    phone = request.POST.get("user_phone") or None
    sex = request.POST.get("user_sex") or None
    user_type = request.POST.get("userType") or None
    specialization = request.POST.get("specialization") or None
    associated_hospital = request.POST.get("hospital") or None
    insurance_provider = request.POST.get("insurance") or None
    password = request.POST.get("password") or None
    address = request.POST.get("address") or None
    borough = request.POST.get("borough") or None
    zip = request.POST.get("zip") or None

    form_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "sex": sex,
        "user_type": user_type,
        "primary_speciality": specialization,
        "associated_hospital": associated_hospital,
        "insurance_provider": insurance_provider,
        "password": password,
        "address": address,
        "borough": borough,
        "zip": zip,
    }

    if not isValidPassword(password):
        return "Error: Invalid Password"

    ret, msg = check_user_validity(form_data)

    if not ret:
        return msg

    return form_data


def user_exists(email):
    return User.objects.filter(username=email).exists()


def create_django_user(email, password, name):
    usr = User.objects.create_user(email, email, password)
    usr.first_name = name
    usr.save()
    return usr


def create_user_profile(user_type, **kwargs):
    if user_type == "doctor":
        valid_fields = {field.name for field in Doctor._meta.get_fields()}
    elif user_type == "patient":
        valid_fields = {field.name for field in Patient._meta.get_fields()}
    elif user_type == "hospital-admin":
        valid_fields = {field.name for field in HospitalAdmin._meta.get_fields()}
    else:
        raise ValueError(f"Invalid user type: {user_type}")
    filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_fields}
    if user_type == "doctor":
        if filtered_kwargs["associated_hospital"] is not None:
            filtered_kwargs["active_status"] = False
        Doctor.objects.create(**filtered_kwargs)
    elif user_type == "patient":
        Patient.objects.create(**filtered_kwargs)
    elif user_type == "hospital-admin":
        filtered_kwargs["active_status"] = False
        HospitalAdmin.objects.create(**filtered_kwargs)


def register(request):
    if request.method == "POST":
        # Collecting data from the form
        form_data = get_form_data(request)
        if type(form_data) is str:
            messages.error(request, form_data)
            return HttpResponseRedirect(reverse("user:user_registration"))
        if user_exists(form_data["email"]):
            messages.error(request, "User already exists! Please go to login page.")
            return HttpResponseRedirect(reverse("user:user_registration"))
        try:
            usr = create_django_user(
                form_data["email"], form_data["password"], form_data["name"]
            )
            user_type = form_data.pop("user_type")
            create_user_profile(user_type, **form_data)
            login(request, usr)
            print("User saved successfully")
        except Exception as e:
            messages.error(
                request,
                "Failed to add new user! Invalid details / User already exists.",
            )
            print(e)
            return render(request, template_name="user/user_registration.html")

        return HttpResponseRedirect(
            reverse("user:home")
        )  # redirect to home page after successful registration

    else:
        hospitals = Hospital.objects.all()
        return render(
            request,
            template_name="user/user_registration.html",
            context={"hospitals": hospitals},
        )


def associate_doctor(request):
    doctor_id = request.POST.get("doctor_id")
    decision = request.POST.get("decision")
    reason = request.POST.get("cancel_reason")
    if Doctor.objects.filter(id=doctor_id).exists():
        doc = Doctor.objects.get(id=doctor_id)
    else:
        messages.error(request, "Doctor does not exist!")
        return redirect("user:account")

    if decision == "APPROVE":
        doc.active_status = True
        doc.save()
    else:
        if not (
            send_email(
                request,
                doc.email,
                "user/approve_reject/template_reject_doctor.html",
                DOCTOR_REJECT_SUBJECT,
                reason=reason,
                hospital_name=doc.associated_hospital,
            )
        ):
            messages.error(request, "Failed to send reject email to doctor.")
        else:
            doc.associated_hospital = None
            doc.active_status = True
            doc.save()

    return redirect("user:account")


def send_email(request, user_email, email_template, subject, **kwargs):
    try:
        user = User.objects.get(email=user_email)
        token_generator = PasswordResetTokenGenerator()
        context = kwargs
        context["user"] = user
        context["domain"] = get_current_site(request).domain
        context["uid"] = urlsafe_base64_encode(user.email.encode("utf-8"))
        context["token"] = token_generator.make_token(user)
        context["protocol"] = "https" if request.is_secure() else "http"
        message = render_to_string(
            email_template,
            context,
        )
        email = EmailMessage(subject, message, to=[user.email])
        if email.send():
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
