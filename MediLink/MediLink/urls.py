from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doctor/', include('doctor.urls')),
    path('hospital/', include('hospital.urls')),
]
