from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Application
from notifications.models import Notification


@receiver(post_save, sender=Application)
def on_application_created(sender, instance: Application, created: bool, **kwargs):
    if not created:
        return
    # 通知岗位发布者：有新申请
    Notification.objects.create(
        recipient=instance.position.posted_by,
        sender=instance.applicant,
        notification_type='application_submitted',
        category='application',
        title='收到新的岗位申请',
        message=f'{getattr(instance.applicant, "real_name", "学生")} 申请了岗位：{instance.position.title}',
        related_model='Application',
        related_object_id=instance.application_id,
        priority='medium',
    )


@receiver(pre_save, sender=Application)
def on_application_status_change(sender, instance: Application, **kwargs):
    if not instance.pk:
        return
    try:
        prev = Application.objects.get(pk=instance.pk)
    except Application.DoesNotExist:
        return
    if prev.status == instance.status:
        return
    # 状态变更通知申请人
    if instance.status in ['accepted', 'rejected']:
        Notification.objects.create(
            recipient=instance.applicant,
            sender=instance.position.posted_by,
            notification_type=f'application_{instance.status}',
            category='application',
            title='申请状态更新',
            message=f'您对“{instance.position.title}”的申请已{ "通过" if instance.status == "accepted" else "被拒" }。',
            related_model='Application',
            related_object_id=instance.application_id,
            priority='medium',
        )


