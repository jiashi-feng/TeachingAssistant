from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Position
from notifications.models import Notification


@receiver(post_save, sender=Position)
def on_position_published(sender, instance: Position, created: bool, **kwargs):
    if created and instance.status == 'open':
        Notification.objects.create(
            recipient=instance.posted_by,
            sender=instance.posted_by,
            notification_type='position_published',
            category='system',
            title='岗位发布成功',
            message=f'您已发布岗位：{instance.title}',
            related_model='Position',
            related_object_id=instance.position_id,
            priority='medium',
        )


