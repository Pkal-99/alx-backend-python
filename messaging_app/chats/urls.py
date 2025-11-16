ffrom django.urls import path, include
from rest_framework.routers import DefaultRouter # Explicitly using DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Setup the router for Conversations
# This creates routes like:
# /conversations/ (GET, POST)
# /conversations/{id}/ (GET, PUT, DELETE)
router = DefaultRouter()
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

# The entire app's URL patterns are now wrapped in the 'api/' path
urlpatterns = [
    path('api/', include([
        # Include all routes registered by the DefaultRouter (e.g., /api/conversations/)
        path('', include(router.urls)),

        # ----------------------------------------------------
        # Nested Routing for Messages (e.g., /api/conversations/{id}/messages/)
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
    ])),
]