from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda req: redirect("/user/home")),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("doctor/", include("doctor.urls")),
    path("hospital/", include("hospital.urls")),
    path("googleMaps/", include("googleMaps.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
