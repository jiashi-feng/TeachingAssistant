"""
学生助教管理平台 - 工时管理模块信号
包含：工时提交通知、工时审核通知
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Timesheet
from notifications.models import Notification


@receiver(post_save, sender=Timesheet)
def on_timesheet_submitted(sender, instance: Timesheet, created: bool, **kwargs):
    """
    工时表提交时，通知岗位发布教师
    """
    if not created:
        return
    
    # 使用 f-string 避免 Windows locale 编码问题
    month_str = f"{instance.month.year}年{instance.month.month:02d}月"

    # 通知岗位发布教师：有助教提交了工时表
    Notification.objects.create(
        recipient=instance.position.posted_by,
        sender=instance.ta,
        notification_type='timesheet_submitted',
        category='timesheet',
        title='收到新的工时表',
        message=f'{instance.ta.real_name} 提交了岗位"{instance.position.title}"在{month_str}的工时表',
        related_model='Timesheet',
        related_object_id=instance.timesheet_id,
        priority='medium',
    )


@receiver(pre_save, sender=Timesheet)
def on_timesheet_status_change(sender, instance: Timesheet, **kwargs):
    """
    工时表状态变更时，通知助教
    """
    if not instance.pk:
        return
    
    try:
        prev = Timesheet.objects.get(pk=instance.pk)
    except Timesheet.DoesNotExist:
        return
    
    # 如果状态没有变化，不发送通知
    if prev.status == instance.status:
        return
    
    # 使用 f-string 避免 Windows locale 编码问题
    month_str = f"{instance.month.year}年{instance.month.month:02d}月"

    # 状态变更通知助教
    if instance.status == 'approved':
        Notification.objects.create(
            recipient=instance.ta,
            sender=instance.reviewed_by or instance.position.posted_by,
            notification_type='timesheet_approved',
            category='timesheet',
            title='工时表已批准',
            message=f'您提交的"{instance.position.title}"在{month_str}的工时表已通过审核。',
            related_model='Timesheet',
            related_object_id=instance.timesheet_id,
            priority='medium',
        )
    elif instance.status == 'rejected':
        Notification.objects.create(
            recipient=instance.ta,
            sender=instance.reviewed_by or instance.position.posted_by,
            notification_type='timesheet_rejected',
            category='timesheet',
            title='工时表被驳回',
            message=f'您提交的"{instance.position.title}"在{month_str}的工时表未通过审核。',
            related_model='Timesheet',
            related_object_id=instance.timesheet_id,
            priority='medium',
        )

