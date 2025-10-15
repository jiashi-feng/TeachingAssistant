"""
学生助教管理平台 - 通知系统模块模型
包含：Notification（通知表）
"""

from django.db import models
from django.conf import settings


class Notification(models.Model):
    """通知表 - 系统消息和通知记录"""
    
    # 通知分类选择
    CATEGORY_CHOICES = [
        ('system', '系统通知'),
        ('application', '申请相关'),
        ('timesheet', '工时相关'),
        ('salary', '薪酬相关'),
    ]
    
    # 优先级选择
    PRIORITY_CHOICES = [
        ('low', '低'),
        ('medium', '中'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]
    
    # 通知类型（详细分类见数据库设计文档）
    TYPE_CHOICES = [
        # 系统通知
        ('system_announcement', '系统公告'),
        ('system_maintenance', '系统维护通知'),
        ('account_activated', '账号激活'),
        ('password_changed', '密码修改'),
        
        # 岗位相关
        ('position_published', '新岗位发布'),
        ('position_updated', '岗位信息更新'),
        ('position_closed', '岗位关闭'),
        ('position_deadline_soon', '申请截止提醒'),
        
        # 申请相关
        ('application_submitted', '收到新申请'),
        ('application_reviewing', '申请审核中'),
        ('application_accepted', '申请通过'),
        ('application_rejected', '申请被拒'),
        ('application_withdrawn', '申请已撤回'),
        
        # 工时相关
        ('timesheet_submitted', '收到工时表'),
        ('timesheet_approved', '工时已批准'),
        ('timesheet_rejected', '工时被驳回'),
        ('timesheet_reminder', '工时提交提醒'),
        
        # 薪酬相关
        ('salary_generated', '薪酬已生成'),
        ('salary_paid', '薪酬已发放'),
        ('salary_delayed', '薪酬延迟通知'),
        
        # 角色相关
        ('role_granted', '角色授予'),
        ('role_revoked', '角色撤销'),
        ('became_ta', '成为助教'),
        
        # 评价相关
        ('evaluation_received', '收到工作评价'),
        ('evaluation_reminder', '评价提醒'),
    ]
    
    notification_id = models.AutoField(
        primary_key=True,
        verbose_name='通知ID'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_notifications',
        verbose_name='接收人'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications',
        verbose_name='发送人',
        help_text='系统通知时为NULL'
    )
    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        verbose_name='通知类型'
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='通知分类'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='标题'
    )
    message = models.TextField(
        verbose_name='消息内容'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        verbose_name='优先级'
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name='是否已读'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='阅读时间'
    )
    related_model = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='关联模型',
        help_text='如: Application, Timesheet, Position'
    )
    related_object_id = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='关联对象ID'
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='过期时间',
        help_text='重要通知不过期（NULL）'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        db_table = 'notification'
        verbose_name = '通知'
        verbose_name_plural = '通知'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        read_status = '已读' if self.is_read else '未读'
        return f'[{read_status}] {self.title} → {self.recipient.real_name}'
    
    def mark_as_read(self):
        """标记为已读"""
        if not self.is_read:
            self.is_read = True
            from django.utils import timezone
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def is_expired(self):
        """判断通知是否过期"""
        if self.expires_at is None:
            return False
        from django.utils import timezone
        return timezone.now() > self.expires_at
