from rest_framework import serializers
from .models import Conversation, Message


class ConversationListSerializer(serializers.ModelSerializer):
    """会话列表：对方姓名、岗位标题、最近消息、未读数"""
    other_name = serializers.SerializerMethodField()
    position_title = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'teacher', 'student', 'position',
            'other_name', 'position_title', 'last_message', 'unread_count',
            'created_at', 'updated_at',
        ]

    def get_other_name(self, obj):
        user = self.context.get('request').user
        return obj.student.real_name if user == obj.teacher else obj.teacher.real_name

    def get_position_title(self, obj):
        return obj.position.title if obj.position else None

    def get_last_message(self, obj):
        last = obj.messages.order_by('-created_at').first()
        if not last:
            return None
        return {'content': last.content[:50], 'created_at': last.created_at, 'sender_id': last.sender_id}

    def get_unread_count(self, obj):
        user = self.context.get('request').user
        return obj.messages.filter(is_read=False).exclude(sender=user).count()


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.real_name', read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'sender_name', 'content', 'is_read', 'created_at', 'read_at']


class SendMessageSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=2000, allow_blank=False)
