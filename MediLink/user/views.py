from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from user.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User as Django_User
# import for email sending
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import secrets
from django.core.mail import EmailMessage
from django.contrib import messages


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
            messages.error(request, 'Incorrect Credentials! User does not exist!')
            return redirect("user:login")
    template_name = "user/login.html"
    return render(request, template_name)

def passwordResetView(request):
    template_name = "user/resetPassword/password_reset.html"

    if request.method == "GET":
        return render(request, template_name)

    else:
        user_email = request.POST.get("user_email")
        print(user_email)

        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            subject = "MediLink Account Password Reset Request"
            message = render_to_string("user/resetPassword/template_reset_password.html", {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(user.email.encode("utf-8")),
                'token': secrets.token_hex(16),
                "protocol": 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(subject, message, to=[user.email])
            if email.send():
                alert_message = "Email sent. Please follow the link to reset your password."
                messages.success(request, alert_message)
                return HttpResponseRedirect(reverse("user:login"))
            else:
                alert_message = "Fail to send an email. Please try again."
                messages.error(request, alert_message)
                return HttpResponseRedirect(reverse("user:passwordReset"))
        
        else:
            alert_message = "Email not exists in our database. Please register a new account."
            messages.error(request, alert_message)
            return HttpResponseRedirect(reverse("user:user_registration"))

def passwordResetConfirmView(request, uidb64, token):
    template_name = "user/resetPassword/password_reset_confirm.html"
    if request.method == "GET":
        return render(request, template_name, {"uidb64": uidb64, "token": token})
    
    else:
        user_email = urlsafe_base64_decode(uidb64).decode("utf-8")
        new_password = request.POST.get("password")
        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            user.password = new_password
            user.save()
            alert_message = "Password reset successfully, please login."
            # return render(request, "user/login.html", {'alert_message': alert_message})
            messages.success(request, alert_message)
            return HttpResponseRedirect(reverse("user:login"))

        else:
            alert_message = "Some error exists when resetting your password, please try again."
            messages.error(request, alert_message)
            return HttpResponseRedirect(reverse("user:passwordReset"))

    

def home(request):
    return render(request, "user/home.html")


def register(request):
    if request.method == "POST":
        # Collecting data from the form
        name = request.POST.get('user_name')
        email = request.POST.get('user_email')
        phone = request.POST.get('user_phone')
        sex = request.POST.get('user_sex')
        user_type = request.POST.get('userType')
        specialization = request.POST.get('specialization') or None
        associated_hospital = request.POST.get('associatedHospital') or None
        insurance_provider = request.POST.get('insurance') or None
        password = request.POST.get('password')  # hashing the password for security

        # Conditionally set fields based on user type
        if user_type != 'doctor':
            specialization = None
        if user_type not in ['doctor', 'hospital-admin']:
            associated_hospital = None
        if user_type != 'patient':
            insurance_provider = None
        
        try:
            Django_User.objects.get(username=email)
            messages.error(request, "User already exists! Please go to login page.")
            return HttpResponseRedirect(reverse("user:user_registration"))
        except:
            pass

        # Create a new user object and save it
        try:
            usr = Django_User.objects.create_user(email, email, password)
            usr.first_name = name
            usr.save()
            
            user = User(
                name=name,
                email=email,
                phone=phone,
                sex=sex,
                user_type=user_type,
                specialization=specialization,
                associated_hospital=associated_hospital,
                insurance_provider=insurance_provider,
                password=password
            )
            user.save()
            print("User saved successfully")
        except Exception as e:
            messages.error(request, "Failed to add new user! Invalid details / User already exists.")
            print(e)
            return render(request, template_name="user/user_registration.html")
            
        return HttpResponseRedirect(reverse("user:home"))  # redirect to home page after successful registration

    return render(request, template_name="user/user_registration.html")
