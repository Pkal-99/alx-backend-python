from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class NotificationTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='12345')
        self.receiver = User.objects.create_user(username='receiver', password='12345')

    def test_notification_creation(self):
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content='Hello!')
        notification = Notification.objects.get(message=message)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)