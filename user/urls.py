from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("registration/", views.register, name="user_registration"),
    path("login/", views.loginView, name="login"),
    path("home/", views.home, name="home"),
    path("passwordReset/", views.passwordResetView, name="passwordReset"),
    path("logout/", views.logoutView, name="logout"),
    path(
        "passwordResetConfirm/<uidb64>/<token>",
        views.passwordResetConfirmView,
        name="passwordResetConfirm",
    ),
    path("account/", views.accountView, name="account"),
    path("cancelAppointment/", views.cancelAppointment, name="cancelAppointment"),
    path("confirmAppointment/", views.confirmAppointment, name="confirmAppointment"),
    path("associateDoctor/", views.associate_doctor, name="associate_doctor")
]
