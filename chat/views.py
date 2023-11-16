# chat/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm
from django.db.models import Q


@login_required
def chat(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(recipient=recipient))
        | (Q(sender=recipient) & Q(recipient=request.user))
    ).order_by("timestamp")

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            Message.objects.create(
                sender=request.user, recipient=recipient, content=message
            )
            return redirect("chat", recipient_id=recipient_id)
    else:
        form = MessageForm()

    return render(
        request,
        "chat/index.html",
        {"recipient": recipient, "messages": messages, "form": form},
    )
