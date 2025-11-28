from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Message

@login_required
@cache_page(60 * 1)  # Cache the view for 60 seconds
def conversation_view(request, message_id):
    # Fetch the conversation messages and replies using the custom manager
    message = get_object_or_404(Message.objects.select_related('sender', 'receiver').prefetch_related('replies'), id=message_id)
    
    # If you're retrieving more messages related to the conversation, fetch them here as well

    return render(request, 'messaging/conversation.html', {'message': message})