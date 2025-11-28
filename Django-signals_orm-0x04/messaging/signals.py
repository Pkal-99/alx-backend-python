from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)
                
            
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.content != instance.content:  # Check if content has changed
            MessageHistory.objects.create(
                message=old_instance,
                old_content=old_instance.content,
                edited_by=old_instance.sender  # Store who last edited it
            )
            instance.edited = True
            instance.edited_at = timezone.now()  # Set the edit timestamp
            instance.edited_by = old_instance.sender  # Set the user who edited
            
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete all messages sent by or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications associated with the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories related to messages by the user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()

