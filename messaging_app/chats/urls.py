from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import ConversationViewSet, MessageViewSet

# Setup the router for Conversations

router = SimpleRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Define the nested URL pattern for messages

message_list = MessageViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

# This pattern will match: /conversations/{conversation_pk}/messages/{pk}/
message_detail = MessageViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    # Include all routes registered by the SimpleRouter
    path('', include(router.urls)),

    # ----------------------------------------------------
    # Nested Routing for Messages
    # The 'conversation_pk' is passed to MessageViewSet.kwargs in views.py
    # ----------------------------------------------------
    path(
        'conversations/<int:conversation_pk>/messages/', 
        message_list, 
        name='message-list'
    ),
    path(
        'conversations/<int:conversation_pk>/messages/<int:pk>/', 
        message_detail, 
        name='message-detail'
    ),
]