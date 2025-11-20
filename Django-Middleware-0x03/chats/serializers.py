from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_picture', 'bio']
        read_only_fields = ['id', 'username', 'email']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Include sender details in nested form

    class Meta:
        model = Message
        fields = ['id', 'sender', 'conversation', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)  # Include participant details in nested form
    messages = MessageSerializer(many=True, read_only=True, source='messages')  # Include messages in nested form

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'messages']
        read_only_fields = ['id', 'created_at']
