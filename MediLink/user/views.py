from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from user.models import User


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
