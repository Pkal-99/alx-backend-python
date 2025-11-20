from django.contrib.auth.models import AbstractUser
from django.db import models

# User Model
class User(AbstractUser):
    """
    Extending the AbstractUser model to add custom fields.
    """
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


# Conversation Model
class Conversation(models.Model):
    """
    Model to track conversations between users.
    """
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} with {self.participants.count()} participants"


# Message Model
class Message(models.Model):
    """
    Model to represent a message in a conversation.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username}"
