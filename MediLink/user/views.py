from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def LoginView(request):
    template_name = 'user/login.html'
    return render(request, template_name)