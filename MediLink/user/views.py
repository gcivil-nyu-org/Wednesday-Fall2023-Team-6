from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def loginView(request):
    template_name = 'user/login.html'
    return render(request, template_name)

def restPwdView(request):
    template_name = 'user/resetPwd.html'
    return render(request, template_name)
        
def register(request):
    if request.method == 'GET':
        return render(request, template_name = 'user/user_registration.html')
    else:
        print(request.POST)
        return HttpResponseRedirect(reverse('user:user_registration'))