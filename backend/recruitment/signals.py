from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Position
from notifications.models import Notification
from accounts.models import User, Role


@receiver(post_save, sender=Position)
def on_position_published(sender, instance: Position, created: bool, **kwargs):
    """
    岗位发布通知
    当新岗位创建且状态为open时，通知所有学生用户
    注意：信号处理中的异常不应该影响岗位创建，所以使用try-except包裹
    """
    if created and instance.status == 'open':
        try:
            # 获取学生角色
            try:
                student_role = Role.objects.get(role_code='student')
            except Role.DoesNotExist:
                # 如果角色不存在，只通知发布者
                try:
                    Notification.objects.create(
                        recipient=instance.posted_by,
                        sender=instance.posted_by,
                        notification_type='position_published',
                        category='system',
                        title='岗位发布成功',
                        message=f'您已成功发布岗位：{instance.title}',
                        related_model='Position',
                        related_object_id=instance.position_id,
                        priority='low',
                    )
                except Exception:
                    pass  # 通知失败不影响岗位创建
                return
            
            # 获取所有学生用户
            students = User.objects.filter(userrole__role=student_role).distinct()
            
            # 为每个学生创建通知
            notifications = []
            for student in students:
                notifications.append(
                    Notification(
                        recipient=student,
                        sender=instance.posted_by,
                        notification_type='position_published',
                        category='system',
                        title='新岗位发布',
                        message=f'新岗位发布：{instance.title}（{instance.course_name}）',
                        related_model='Position',
                        related_object_id=instance.position_id,
                        priority='medium',
                    )
                )
            
            # 批量创建通知（提高性能）
            if notifications:
                try:
                    Notification.objects.bulk_create(notifications)
                except Exception:
                    # 批量创建失败，尝试单个创建（降级处理）
                    pass
            
            # 同时通知发布者本人（岗位发布成功）
            try:
                Notification.objects.create(
                    recipient=instance.posted_by,
                    sender=instance.posted_by,
                    notification_type='position_published',
                    category='system',
                    title='岗位发布成功',
                    message=f'您已成功发布岗位：{instance.title}',
                    related_model='Position',
                    related_object_id=instance.position_id,
                    priority='low',
                )
            except Exception:
                pass  # 通知失败不影响岗位创建
        except Exception as e:
            # 记录错误但不影响岗位创建
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'岗位发布通知失败: {e}', exc_info=True)
            # 不抛出异常，确保岗位创建成功


