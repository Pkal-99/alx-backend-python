from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter, OrderingFilter # NEW: Import Filters
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend # NEW: Import Django Filter
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    - list: Returns all conversations the authenticated user is a participant of.
    - retrieve: Returns a specific conversation, including all its messages.
    - create: Creates a new conversation.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    
    # NEW: Integrate DRF Filters
    filter_backends = [SearchFilter, OrderingFilter]
    
    # Allows searching conversations by participant username
    # Note: 'participants__username' traverses the Many-to-Many relationship
    search_fields = ['participants__username'] 
    
    # Allows ordering results by updated_at or created_at
    ordering_fields = ['updated_at', 'created_at']
    ordering = ['-updated_at'] # Default ordering

    def get_queryset(self):
        """
        Filters conversations to only include those where the requesting user is a participant.
        """
        # The 'participants' M2M field is automatically filtered against the current user
        return Conversation.objects.filter(participants=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        """
        Handles conversation creation. Ensures the requesting user is included in the participants.
        """
        participant_ids = serializer.validated_data.get('participant_ids', [])
        current_user_id = self.request.user.id
        
        # Ensure the current user is always included in the participants set
        if current_user_id not in participant_ids:
            participant_ids.append(current_user_id)
            
        # The serializer's validation ensures there are unique participants (at least 2, including the user)
        # We pass the cleaned list back for the serializer's create method to handle M2M setup.
        serializer.validated_data['participant_ids'] = list(set(participant_ids))
        
        serializer.save()

# --- 2. Message ViewSet (Nested within Conversation) ---
class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be listed (within a conversation) 
    or created (sending a new message).
    
    Supports filtering messages by 'is_read' status.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    
    # NEW: Integrate DjangoFilterBackend
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    # Allows filtering by boolean field 'is_read'
    filterset_fields = ['is_read'] 
    ordering_fields = ['timestamp']
    ordering = ['timestamp']
    
    # We will fetch the conversation ID from the URL context set by the router (later in urls.py)
    def get_conversation_context(self):
        """Helper to get the parent conversation object based on URL lookup."""
        conversation_pk = self.kwargs.get('conversation_pk')
        if not conversation_pk:
            # For POST requests to the list endpoint, we don't need the context yet
            if self.action == 'create': 
                return None
            
            raise serializers.ValidationError({"conversation": "Conversation ID is required."})
            
        conversation = get_object_or_404(Conversation, pk=conversation_pk)
        
        # Security check: Ensure the requesting user is part of the conversation
        if not conversation.participants.filter(pk=self.request.user.pk).exists():
            raise PermissionDenied("You are not a participant of this conversation.")
            
        return conversation

    def get_queryset(self):
        """
        Filters messages to only show those belonging to the specified, authorized conversation.
        """
        conversation = self.get_conversation_context()
        if conversation:
            # We explicitly order by timestamp here, though OrderingFilter is also enabled.
            return Message.objects.filter(conversation=conversation).order_by('timestamp')
        return Message.objects.none()

    def perform_create(self, serializer):
        """
        Sets the sender to the authenticated user and links the message to the conversation.
        """
        conversation = self.get_conversation_context()
        if not conversation:
            # This check is now redundant due to the check in get_conversation_context, 
            # but kept for explicit clarity in the creation path.
            raise serializers.ValidationError({"conversation": "Conversation ID is required."})
            
        # Automatically set the sender to the current authenticated user
        serializer.save(sender=self.request.user, conversation=conversation)