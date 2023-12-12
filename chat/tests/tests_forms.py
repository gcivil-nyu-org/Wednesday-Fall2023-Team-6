from django.test import TestCase
from chat.forms import MessageForm


class MessageFormTestCase(TestCase):
    def test_valid_form(self):
        # Create a form instance with valid data
        form_data = {
            "content": "Test content",
            "attachment": None,  # You can attach a file if needed
        }
        form = MessageForm(data=form_data)

        # Assert that the form is valid
        self.assertTrue(form.is_valid())

    def test_save_form(self):
        # Create a form instance with valid data
        form_data = {
            "content": "Test content",
            "attachment": None,
        }
        form = MessageForm(data=form_data)

        # Save the form as a model instance
        if form.is_valid():
            message = form.save()

            # Verify that the saved instance has the correct data
            self.assertEqual(message.content, form_data["content"])
            self.assertEqual(message.attachment, form_data["attachment"])
