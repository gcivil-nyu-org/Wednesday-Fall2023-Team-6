from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from doctor.models import Doctor
from user.models import Patient
from .models import ChatSession


def index(request):
    return render(request, "chat/index.html")


#
# def room(request, room_name):
#     return render(request, "chat/room.html", {"room_name": room_name})


# @login_required
def start_chat(request):
    # Ensure that the logged-in user is either the doctor or the patient
    # if request.user.id != doctor_id and request.user.id != patient_id:
    #     return redirect("some_error_page")  # Redirect to an error page or similar
    #
    # # Get the doctor and patient objects
    # doctor = get_object_or_404(Doctor, pk=doctor_id)
    # patient = get_object_or_404(Patient, pk=patient_id)

    # Create a new ChatSession object or get an existing one
    # chat_session, created = ChatSession.objects.get_or_create(
    #     # doctor=doctor, patient=patient
    # )
    chat_session = ChatSession.objects.create()
    print(chat_session.id)
    # Redirect to the chat room for this session
    return redirect("chat_room", session_id=chat_session.id)


# @login_required
def chat_room(request, session_id):
    # Get the chat session object
    chat_session = get_object_or_404(ChatSession, pk=session_id)

    # # Ensure that the logged-in user is part of the chat session
    # if (
    #     request.user != chat_session.doctor.user
    #     and request.user != chat_session.patient.user
    # ):
    #     return redirect("some_error_page")  # Redirect to an error page or similar

    # Render the chat room template with the session context
    return render(
        request,
        "chat/room.html",
        {
            "session_id": chat_session.id,
            # "doctor": chat_session.doctor,
            # "patient": chat_session.patient,
        },
    )


# def chat_room(request, session_id):
#     session = get_object_or_404(ChatSession, pk=session_id)
#     # Ensure that the user is either the doctor or the patient in this session
#     # if request.user != session.doctor.user and request.user != session.patient.user:
#     #     return HttpResponseForbidden("You are not allowed to view this chat.")
#     return render(request, "chat/room.html", {"session": session})
