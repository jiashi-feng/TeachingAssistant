"""
学生助教管理平台 - 申请流程模块模型
包含：Application（申请表）
"""

from django.db import models
from django.conf import settings
from recruitment.models import Position


class Application(models.Model):
    """申请表 - 记录学生申请岗位的过程"""
    
    # 申请状态选择
    STATUS_CHOICES = [
        ('submitted', '已提交'),
        ('reviewing', '审核中'),
        ('accepted', '已录用'),
        ('rejected', '已拒绝'),
    ]
    
    application_id = models.AutoField(
        primary_key=True,
        verbose_name='申请ID'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='申请的岗位'
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='申请人'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted',
        verbose_name='申请状态'
    )
    resume = models.FileField(
        upload_to='resumes/%Y/%m/',
        verbose_name='简历文件',
        null=True,
        blank=True
    )
    resume_text = models.TextField(
        null=True,
        blank=True,
        verbose_name='在线填写简历'
    )
    applied_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='申请时间'
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='审核时间'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications',
        verbose_name='审核人'
    )
    review_notes = models.TextField(
        null=True,
        blank=True,
        verbose_name='审核备注'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'application'
        verbose_name = '申请记录'
        verbose_name_plural = '申请记录'
        # 唯一约束：同一个学生不能重复申请同一个岗位
        unique_together = [['position', 'applicant']]
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['applicant']),
            models.Index(fields=['status']),
            models.Index(fields=['applied_at']),
        ]
    
    def __str__(self):
        return f'{self.applicant.real_name} 申请 {self.position.title}'
    
    def is_pending(self):
        """判断申请是否待审核"""
        return self.status in ['submitted', 'reviewing']
    
    def is_accepted(self):
        """判断申请是否已录用"""
        return self.status == 'accepted'
    
    def is_rejected(self):
        """判断申请是否已拒绝"""
        return self.status == 'rejected'
