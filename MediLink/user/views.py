from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('user_email')
        password = request.POST.get('user_pwd')
        #print(username,password)
        user = authenticate(request, username=username, password=password)

        if user is not None:
             login(request, user)
             print("Login successful")
             return redirect('home')  # Redirect to the home page after login
        
        else:
            return HttpResponse ("Username or Password is incorrect!!!!")
    template_name = 'user/login.html'
    return render(request, template_name)

def restPwdView(request):
    template_name = 'user/resetPwd.html'
    return render(request, template_name)

def home(request):
    return render(request, 'user/home.html')
        
def register(request):
    if request.method == 'GET':
        return render(request, template_name = 'user/user_registration.html')
    else:
        print(request.POST)
        return HttpResponseRedirect(reverse('user:user_registration'))