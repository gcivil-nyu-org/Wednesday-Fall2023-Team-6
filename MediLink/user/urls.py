from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('registration/', views.register, name='user_registration'),
    path('login/', views.loginView, name='login'),
    path('resetPassword/', views.restPwdView, name='resetPassword'),
    path('home/', views.home, name='home'),

]