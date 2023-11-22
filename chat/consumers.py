import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from doctor.models import DoctorAppointment
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.appointment = await self.get_appointment(int(self.room_name))
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["content"]
        has_attachment = data["has_attachment"]
        sender = await self.get_sender(self.user.username)
        if has_attachment == "no":
            await self.save_message(sender, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
                "sender": sender,
                "has_attachment": has_attachment,
            },
        )

    @sync_to_async
    def save_message(self, sender, content):
        Message.objects.create(
            appointment=self.appointment, sender=sender, content=content
        )

    @sync_to_async
    def get_appointment(self, id):
        return DoctorAppointment.objects.get(id=id)

    @sync_to_async
    def get_sender(self, username):
        if username == self.appointment.patient.email:
            sender = "pat"
        elif username == self.appointment.doctor.email:
            sender = "doc"
        else:
            raise Exception("Invalid user")

        return sender

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        has_attachment = event["has_attachment"]
        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"message": message, "sender": sender, "has_attachment": has_attachment}
            )
        )
