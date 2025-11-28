from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Message


#@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # This will trigger the post_delete signal
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # Redirect to the homepage or desired location

    return render(request, 'messaging/delete_user.html')  # Create a template for confirmation


@login_required
def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        receiver_id = request.POST.get('receiver_id')
        
        # Ensure the receiver exists
        receiver = get_object_or_404(User, id=receiver_id)
        
        # Create the message
        Message.objects.create(sender=request.user, receiver=receiver, content=content)
        messages.success(request, "Message sent successfully!")
        
        return redirect('home')  # Redirect after sending

    return render(request, 'messaging/send_message.html')  # Create a form for sending messages

@login_required
def conversation_view(request, message_id):
    # Fetch the message and its replies using select_related and prefetch_related
    message = get_object_or_404(Message.objects.select_related('sender', 'receiver').prefetch_related('replies'), id=message_id)

    return render(request, 'messaging/conversation.html', {'message': message})

@login_required
def sent_messages_view(request):
    messages = Message.objects.filter(sender=request.user).select_related('receiver')
    return render(request, 'messaging/sent_messages.html', {'messages': messages})

@login_required
def received_messages_view(request):
    messages = Message.objects.filter(receiver=request.user).select_related('sender')
    return render(request, 'messaging/received_messages.html', {'messages': messages})



@login_required
def inbox_view(request):
    unread_messages = Message.unread_messages.for_user(request.user)  # Use the custom manager
    
    return render(request, 'messaging/inbox.html', {'unread_messages': unread_messages})