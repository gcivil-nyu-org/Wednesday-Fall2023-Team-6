from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda req: redirect("/user/home")),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("doctor/", include("doctor.urls")),
    path("hospital/", include("hospital.urls")),
]
