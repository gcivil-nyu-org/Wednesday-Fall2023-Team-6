from django.urls import path
from . import views

app_name = 'hospital'
urlpatterns = [
    path('<int:pk>/', views.HospitalDetailView.as_view(), name='detail_view'),
    path('<int:pk>/bookAppointment', views.book_appointment, name='book_appointment'),
]