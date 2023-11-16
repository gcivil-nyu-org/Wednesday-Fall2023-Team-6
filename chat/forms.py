from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Type your message..."})
    )
