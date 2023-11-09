import re
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login
from user.models import Choices, Patient
from doctor.models import Doctor, DoctorAppointment
from hospital.models import HospitalAdmin, Hospital, HospitalAppointment
from django.contrib.auth.models import User

# import for email sending
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import logout

# import for avatar changing
import os
from django.conf import settings


PASSWORD_RESET_SUBJECT = "MediLink Account Password Reset Request"


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
        token_generator = PasswordResetTokenGenerator()

        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            subject = PASSWORD_RESET_SUBJECT
            message = render_to_string(
                "user/resetPassword/template_reset_password.html",
                {
                    "user": user,
                    "domain": get_current_site(request).domain,
                    "uid": urlsafe_base64_encode(user.email.encode("utf-8")),
                    "token": token_generator.make_token(user),
                    "protocol": "https" if request.is_secure() else "http",
                },
            )
            email = EmailMessage(subject, message, to=[user.email])
            if email.send():
                alert_message = (
                    "Email sent. Please follow the link to reset your password."
                )
                messages.success(request, alert_message)
                return HttpResponseRedirect(reverse("user:login"))
            else:
                alert_message = "Fail to send an email. Please try again."
                messages.error(request, alert_message)
                return HttpResponseRedirect(reverse("user:passwordReset"))

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
    return render(request, "user/home.html")


def accountView(request):
    template_name = "user/account.html"
    """
    check weather a user is logged in
    for the account view
    """
    if request.user.is_authenticated:
        user = request.user
        if user.username != "admin":
            patient = Patient.objects.filter(email=user.email)
            doctor = Doctor.objects.filter(email=user.email)
            hospital_admin = HospitalAdmin.objects.filter(email=user.email)

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
            elif len(doctor) != 0:
                login_user = doctor.first()
                userType = "doctor"
                doctor_appointments = DoctorAppointment.objects.filter(
                    doctor=login_user
                )
                hospital_appointments = HospitalAppointment.objects.filter(
                    preferred_doctor=login_user
                )
            else:
                login_user = hospital_admin.first()
                userType = "hospitalAdmin"
                doctor_appointments = DoctorAppointment.objects.filter(
                    doctor=login_user
                )
                hospital_appointments = HospitalAppointment.objects.filter(
                    preferred_doctor=login_user
                )
            print(doctor_appointments)
            print(hospital_appointments)

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
                    },
                )
            else:
                # -------------- Upload Avatar --------------
                if len(request.FILES) > 0:
                    uploaded_file = request.FILES["avatar"]
                    MAX_FILE_SIZE_KB = 50

                    # Check if the uploaded file size exceeds the maximum allowed size
                    if (
                        uploaded_file.size > MAX_FILE_SIZE_KB * 1024
                    ):  # Convert KB to bytes
                        return HttpResponseBadRequest(
                            "File size is too large. Maximum allowed size is {} KB.".format(
                                MAX_FILE_SIZE_KB
                            )
                        )

                    login_user.avatar = uploaded_file
                    login_user.save()
                    file_path = os.path.join(
                        settings.MEDIA_ROOT, "avatars", uploaded_file.name
                    )

                    # Save the uploaded file to the specified path
                    with open(file_path, "wb+") as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)

                    return redirect("user:account")

                # -------------- Edit Account Info --------------
                else:
                    login_user.name = request.POST.get("name")
                    login_user.phone = request.POST.get("phone")
                    login_user.sex = request.POST.get("sex")
                    login_user.insurance_provider = request.POST.get("insurance")
                    login_user.address = request.POST.get("address")
                    login_user.borough = request.POST.get("borough")
                    login_user.zip = request.POST.get("zip")
                    login_user.save()
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

    if not name:
        return "Error: Invalid Name"
    if not isValidEmail(email):
        return "Error: Invalid Email"
    if not phone:
        return "Error: Invalid Phone"
    if sex not in [opt[0] for opt in Choices.sex]:
        return "Error: Invalid Sex"
    if user_type not in ["patient", "doctor", "hospital-admin"]:
        return "Error: Invalid User Type"
    if not isValidPassword(password):
        return "Error: Invalid Password"
    if not address:
        return "Invalid Address"
    if not zip:
        return "Invalid Zip"
    if borough not in [opt[0] for opt in Choices.boroughs]:
        return "Error: Invalid Borough"

    # Conditionally set fields based on user type
    if user_type != "doctor":
        specialization = None
    if user_type not in ["doctor", "hospital-admin"]:
        associated_hospital = None
    elif user_type == "doctor" and (not associated_hospital):
        associated_hospital = None
    else:
        try:
            associated_hospital = Hospital.objects.get(id=int(associated_hospital))
        except Exception as e:
            print("Error: ", e)
            return "Error: Invalid Hospital selected."
    if user_type != "patient":
        insurance_provider = None

    return {
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
        Doctor.objects.create(**filtered_kwargs)
    elif user_type == "patient":
        Patient.objects.create(**filtered_kwargs)
    elif user_type == "hospital-admin":
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

    return render(request, template_name="user/user_registration.html")
