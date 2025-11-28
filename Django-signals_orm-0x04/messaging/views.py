from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages

#@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # This will trigger the post_delete signal
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # Redirect to the homepage or desired location

    return render(request, 'messaging/delete_user.html')  # Create a template for confirmation


def conversation_view(request, message_id):
    # Fetch the message and its replies using prefetch_related
    message = Message.objects.select_related('sender', 'receiver').prefetch_related('replies').get(id=message_id)
    
    return render(request, 'messaging/conversation.html', {'message': message})

def get_replies(message):
    replies = message.replies.all()  # Fetch the replies for the message
    threaded_replies = []
    
    for reply in replies:
        nested_replies = get_replies(reply)  # Recursive call to get replies for this reply
        threaded_replies.append({'message': reply, 'replies': nested_replies})
    
    return threaded_replies