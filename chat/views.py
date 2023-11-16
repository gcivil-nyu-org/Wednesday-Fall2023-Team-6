from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import MessageForm
from .models import Message
from django.db.models import Q


@login_required
def chat(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=recipient) | Q(sender=recipient, recipient=request.user)
    ).order_by("timestamp")

    if request.method == "POST":
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect("chat", recipient_id=recipient_id)
    else:
        form = MessageForm()

    return render(
        request,
        "chat/index.html",
        {
            "recipient": recipient,
            "recipient_id": recipient_id,  # Ensure this context variable is set
            "messages": messages,
            "form": form,
        },
    )
