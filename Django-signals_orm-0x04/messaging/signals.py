from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.db.models.signals import pre_save


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