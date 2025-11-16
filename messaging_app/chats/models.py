# chat/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # To import the User model
import uuid
from django.utils import timezone


# Create your models here.
# Get the User model configured in settings.AUTH_USER_MODEL
User = settings.AUTH_USER_MODEL

""" User with roles class """
class CustomUser(AbstractUser):
    """
    Extends the AbstractUser model for additional fields.
    """
""" Extended user model with UUID primary key and additional fields. """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True,)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password', 'role']

    def __str__(self):
        return self.username

""" Conversation class """
class Conversation(models.Model):
    """
    Chat Conversation thread between two or more users.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Many-to-Many relationship: A conversation has many users, 
    # and a user has many conversations.
    participants = models.ManyToManyField(
        User,
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        help_text="The users participating in this conversation."
    )
    
    # Timestamps for tracking
    created_at = models.DateTimeField(auto_now_add=True)
   # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Display the primary keys of the participants for quick identification
        return f"Conversation ID {self.pk}"

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

""" Messaging class """
class Message(models.Model):
    """
    Represents a single message sent by a user within a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Foreign Key: A message belongs to one conversation.
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE, # Deleting a conversation deletes all its messages.
        settings.AUTH_USER_MODEL,
        related_name='Sent messages',
        help_text="The conversation this message belongs to."
    )
    
    # Foreign Key: A message is sent by one user.
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # If the sender is deleted, set their messages' sender to NULL (keeps message history).
        related_name='sent_messages',
        null=True # Allows the sender field to be NULL if the user is deleted
    )
    
    message_body = models.TextField(help_text="The text content of the message.")
    sent_at = models.DateTimeField(auto_now_add=True)
    #is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp'] # Important for displaying messages in correct order
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        
    def __str__(self):
        return f"Msg from {self.sender.username if self.sender else 'Deleted User'} in Conv {self.conversation.pk}"