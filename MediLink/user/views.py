from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from user.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password

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


def restPwdView(request):
    template_name = "user/resetPwd.html"
    if request.method == "GET":
        return render(request, template_name)

    else:
        user_email = request.POST.get("user_email")
        new_password = request.POST.get("password")

        print(user_email, new_password)
        if User.objects.filter(email=user_email).exists():
            user = User.objects.get(email=user_email)
            user.password = new_password
            user.save()
            return HttpResponse("Password is reset!")

        else:
            return HttpResponse("User not exists")


def home(request):
    return render(request, "user/home.html")


def register(request):
    if request.method == "GET":
        return render(request, template_name="user/user_registration.html")
    else:
        print(request.POST)
        return HttpResponseRedirect(reverse("user:user_registration"))

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
        password = make_password(request.POST.get('password'))  # hashing the password for security

        # Conditionally set fields based on user type
        if user_type != 'doctor':
            specialization = None
        if user_type not in ['doctor', 'hospital-admin']:
            associated_hospital = None
        if user_type != 'patient':
            insurance_provider = None

        # Create a new user object and save it
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

        messages.success(request, "Registration successful!")
        return HttpResponseRedirect(reverse("user:login"))  # redirect to login page after successful registration

    return render(request, template_name="user/user_registration.html")
