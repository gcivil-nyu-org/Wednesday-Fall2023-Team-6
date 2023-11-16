# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... other url patterns ...
    path(
        "<int:recipient_id>/", views.chat, name="chat"
    ),  # The 'name' argument should match your template tag.
]
