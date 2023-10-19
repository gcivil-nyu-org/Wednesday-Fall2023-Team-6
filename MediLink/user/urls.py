from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("registration/", views.register, name="user_registration"),
    path("login/", views.loginView, name="login"),
    path("home/", views.home, name="home"),
    path("passwordReset/", views.passwordResetView, name="passwordReset"),
    path(
        "passwordResetConfirm/<uidb64>/<token>",
        views.passwordResetConfirmView,
        name="passwordResetConfirm",
    ),
]
