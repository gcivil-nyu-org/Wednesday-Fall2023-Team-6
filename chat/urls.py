# urls.py
from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    # ... other url patterns ....
    path(
        "<int:appointment_id>/", views.chat, name="chat"
    ),  # The 'name' argument should match your template tag.
]
