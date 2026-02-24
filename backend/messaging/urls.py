from django.urls import path
from .views import ConversationList, StartConversation, MessageList, SendMessage

app_name = 'messaging'

urlpatterns = [
    path('conversations/', ConversationList.as_view(), name='conversation-list'),
    path('start/', StartConversation.as_view(), name='start-conversation'),
    path('conversations/<int:conversation_id>/messages/', MessageList.as_view(), name='message-list'),
    path('conversations/<int:conversation_id>/send/', SendMessage.as_view(), name='send-message'),
]
