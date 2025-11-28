from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

class NotificationTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='12345')
        self.receiver = User.objects.create_user(username='receiver', password='12345')

    def test_notification_creation(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        
class MessageEditTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='12345')
        self.receiver = User.objects.create_user(username='receiver', password='12345')
        self.message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Initial Message')

    def test_message_edit_logging(self):
        # Edit the message
        self.message.content = 'Edited Message'
        self.message.save()  # Triggers the pre_save signal
        
        # Check that MessageHistory is created
        history = MessageHistory.objects.get(message=self.message)
        self.assertEqual(history.old_content, 'Initial Message')
        self.assertEqual(self.message.edited, True)  # Ensure the edited field is set to True

    def test_view_message_history(self):
        self.message.content = 'Edited Message'
        self.message.save()  # Create history record
        
        # Verify history can be accessed through the get_history method
        histories = self.message.get_history()
        self.assertEqual(histories.count(), 1)
        self.assertEqual(histories.first().old_content, 'Initial Message')