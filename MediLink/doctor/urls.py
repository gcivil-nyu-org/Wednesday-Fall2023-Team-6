from django.urls import path
from . import views

app_name = 'doctor'
urlpatterns = [
    path('<int:pk>/', views.DoctorDetailView.as_view(), name='detail_view'),
    path('<int:doctor_id>/bookConsultation', views.book_consultation, name='book_consultation'),
]