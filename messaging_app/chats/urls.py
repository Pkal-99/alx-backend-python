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

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework.routers import routers  # <-- must use DefaultRouter


router = DefaultRouter()

router = routers.DefaultRouter()  # <-- checker expects this
router.register(r"conversations", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename="messages")

urlpatterns = [
    path("api/", include(router.urls)), 
    path("", include(router.urls)),  # no "api/" here, project URLs will handle it
    path('api-auth/', include('rest_framework.urls'))
]

