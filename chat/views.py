import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from doctor.models import Doctor, DoctorAppointment
from user.models import Patient
from django.utils.timezone import now, localtime
from django.contrib import messages

import os
from django.conf import settings
import logging


@login_required
def chat(request, appointment_id):
    appointment = get_object_or_404(DoctorAppointment, id=appointment_id)
    if appointment.status != "CNF":
        messages.error(request, "Error: Appointment not confirmed.")
        return redirect("user:account")

    curr_time = localtime(now())
    if curr_time < appointment.start_time:
        messages.error(request, "Error: Appointment not started yet")
        return redirect("user:account")

    appointment_messages = Message.objects.filter(appointment=appointment).order_by(
        "timestamp"
    )

    current_user = None
    if Patient.objects.filter(email=request.user.username).exists():
        current_user = "pat"
        recipient = appointment.doctor
    elif Doctor.objects.filter(email=request.user.username).exists():
        current_user = "doc"
        recipient = appointment.patient
    else:
        messages.error(request, "Unauthorized User")
        return redirect("user:account")

    if request.method == "POST":
        try:
            message = Message()
            message.content = request.POST.get("content")
            message.sender = current_user
            message.appointment = appointment
            if len(request.FILES["attachment"]) > 0:
                attachment = request.FILES["attachment"]
                message.attachment = attachment

                ext = attachment.name.split(".")[-1]
                attachment_name = f"{uuid.uuid4().hex}.{ext}"
                os.makedirs(
                    os.path.join(settings.MEDIA_ROOT, "attachments"), exist_ok=True
                )
                file_path = os.path.join(
                    settings.MEDIA_ROOT, "attachments", attachment_name
                )
                # Save the uploaded file to the specified path
                with open(file_path, "wb+") as destination:
                    for chunk in attachment.chunks():
                        destination.write(chunk)

                message.full_clean()
                message.save()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error("Post error", e)
            messages.error(request, e)
            return redirect("user:account")

    return render(
        request,
        "chat/chats.html",
        {
            "recipient": recipient,
            "appointment_id": appointment_id,
            "current_user": current_user,  # Ensure this context variable is set
            "messages": appointment_messages,
        },
    )
