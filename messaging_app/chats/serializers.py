# serializers.py 
from rest_framework import serializers
from .models import User, Message, Conversation
"""
Converting Python objects and data structures into a format that can 
be stored, transmitted, or reconstructed later. JSON
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    # Explicitly define content using CharField for length validation
    content = serializers.CharField(max_length=500, help_text="The text content of the message.")
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation', 'content', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
"""
["serializers.CharField", "serializers.SerializerMethodField()", "serializers.ValidationError"]
"""

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    # Nested serializer to display the messages within this conversation
    messages = MessageSerializer(many=True, read_only=True)
    
    # NEW: SerializerMethodField to display a quick preview of the last message 
    last_message_preview = serializers.SerializerMethodField()
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'last_message_preview', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']


class ConversationCreateSerializer(serializers.ModelSerializer):
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']

    def get_last_message_preview(self, obj):
        """
        Retrieves the content of the most recent message in the conversation.
        """
        last_message = obj.messages.all().order_by('-timestamp').first()
        if last_message:
            # Return a truncated version for a clean preview
            return f"{last_message.sender.username}: {last_message.content[:50]}..."
        return "No messages yet."

    def validate_participant_ids(self, value):
        """
        Uses serializers.ValidationError to ensure a conversation
        has at least two unique participants.
        """
        # Ensure there are unique IDs (set conversion removes duplicates)
        unique_ids = set(value)
        
        if len(unique_ids) < 2:
            raise serializers.ValidationError("A conversation must have at least two unique participants.")
            
        # Ensure all provided IDs actually exist as users
        existing_users = CustomUser.objects.filter(id__in=unique_ids)
        if len(existing_users) != len(unique_ids):
             raise serializers.ValidationError("One or more provided user IDs do not correspond to an existing user.")
             
        return unique_ids

    def create(self, validated_data):
        """
        Custom create method to handle the many-to-many relationship 
        for participants after the conversation is created.
        """
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participant_ids)
        return conversation
