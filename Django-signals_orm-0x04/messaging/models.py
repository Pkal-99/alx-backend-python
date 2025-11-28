from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # New field to track edits
    edited_at = models.DateTimeField(null=True, blank=True)  # To track when it was edited
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'
    
    def get_history(self):
        return self.history.all()  # Returns all history entries for this message  

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user} - Message ID {self.message.id}'

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_on = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'History of message {self.message.id} by {self.edited_by} on {self.edited_on}'
    

    

