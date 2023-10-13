from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('registration/', views.register, name='user_registration'),
]