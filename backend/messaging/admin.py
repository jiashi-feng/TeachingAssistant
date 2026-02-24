from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['conversation_id', 'teacher', 'student', 'position', 'created_at']
    list_filter = ['created_at']
    search_fields = ['teacher__real_name', 'student__real_name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'conversation', 'sender', 'content_short', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']

    def content_short(self, obj):
        return (obj.content or '')[:50]
    content_short.short_description = '内容'
