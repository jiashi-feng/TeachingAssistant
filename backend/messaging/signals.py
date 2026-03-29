"""
新聊天消息 -> 为会话对方创建站内通知（与 notifications 模块联动）
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from notifications.models import Notification

from .models import Message


@receiver(post_save, sender=Message)
def notify_recipient_on_new_message(sender, instance: Message, created: bool, **kwargs):
    if not created:
        return
    conv = instance.conversation
    if instance.sender_id == conv.teacher_id:
        recipient = conv.student
    else:
        recipient = conv.teacher
    sender_name = getattr(instance.sender, 'real_name', '对方')
    preview = instance.content.strip()
    if len(preview) > 200:
        preview = preview[:200] + '...'
    try:
        Notification.objects.create(
            recipient=recipient,
            sender=instance.sender,
            notification_type='chat_new_message',
            category='chat',
            title=f'{sender_name} 发来新消息',
            message=preview or '（空消息）',
            related_model='Conversation',
            related_object_id=conv.conversation_id,
            priority='medium',
        )
    except Exception:
        # 聊天消息已落库，通知失败不应阻断发送流程
        pass
