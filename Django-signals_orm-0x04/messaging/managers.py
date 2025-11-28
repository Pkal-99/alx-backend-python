from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        # Optimize by retrieving only necessary fields
        return self.filter(receiver=user, read=False).only('id', 'content', 'timestamp', 'sender')