from django.urls import path, include
from rest_framework.routers import DefaultRouter
# Assuming rest_framework_nested is available for cleaner nested routing
from rest_framework_nested import routers 
from .views import ConversationViewSet, MessageViewSet
"""
# --- 1. Base Router (Handles /conversations/) ---
# Setup the router for Conversations
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# --- 2. Nested Router (Handles /conversations/{id}/messages/) ---
# The lookup field is 'conversation' which corresponds to the parent resource in the URL
# The conversation_pk will be available in the MessageViewSet via self.kwargs['conversation_pk']
conversations_router = routers.NestedDefaultRouter(
    router, 
    r'conversations', 
    lookup='conversation'
)

# Register the messages endpoint nested under the conversations
conversations_router.register(
    r'messages', 
    MessageViewSet, 
    basename='conversation-messages'
)

"""

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# The entire app's URL patterns are now wrapped in the 'api/' path
urlpatterns = [
    path('api/v1/', include([ # ADDED: v1 versioning back for best practice
        # Include all base routes (e.g., /api/v1/conversations/)
        path('', include(router.urls)),

        # Include all nested routes (e.g., /api/v1/conversations/{id}/messages/)
        path('', include(conversations_router.urls)),
    ])),
]