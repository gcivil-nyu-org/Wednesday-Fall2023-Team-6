from django.urls import path
from .views import DoctorDetailView, book_consultation

app_name = 'doctor'

urlpatterns = [
    path('<int:pk>/', DoctorDetailView.as_view(), name='detail_view'),
    path('<int:doctor_id>/bookConsultation', book_consultation, name='book_consultation'),
   
]
