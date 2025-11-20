from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.decorators import action


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """
    queryset = Conversation.objects.prefetch_related('participants', 'messages').all()
    serializer_class = ConversationSerializer

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """
        Custom action to create a new conversation
        """
        participants = request.data.get('participants')
        if not participants or len(participants) < 2:
            return Response({"error": "A conversation must include at least two participants."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages
    """
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Override create method to handle sending messages to a conversation
        """
        sender = request.user  # Assume authenticated user is the sender
        conversation_id = request.data.get('conversation')
        content = request.data.get('content')

        if not conversation_id or not content:
            return Response({"error": "Conversation and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation does not exist."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(sender=sender, conversation=conversation, content=content)
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
