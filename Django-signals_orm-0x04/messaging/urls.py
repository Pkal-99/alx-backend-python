from django.urls import path
from .views import delete_user, inbox_view
from .views import send_message, conversation_view, sent_messages_view, received_messages_view

urlpatterns = [
    # other paths
    path('delete_user/', delete_user, name='delete_user'),
    path('send_message/', send_message, name='send_message'),
    path('conversation/<int:message_id>/', conversation_view, name='conversation_view'),
    path('sent_messages/', sent_messages_view, name='sent_messages'),
    path('received_messages/', received_messages_view, name='received_messages'),
    path('inbox/', inbox_view, name='inbox'),

]

 