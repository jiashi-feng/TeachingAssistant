"""
学生助教管理平台 - 招募管理模块模型
包含：Position（岗位表）
"""

from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Position(models.Model):
    """岗位表 - 存储教师发布的助教岗位信息"""
    
    # 岗位状态选择
    STATUS_CHOICES = [
        ('open', '开放中'),
        ('closed', '已关闭'),
        ('filled', '已招满'),
    ]
    
    position_id = models.AutoField(
        primary_key=True,
        verbose_name='岗位ID'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='岗位标题'
    )
    course_name = models.CharField(
        max_length=100,
        verbose_name='课程名称'
    )
    course_code = models.CharField(
        max_length=20,
        verbose_name='课程代码'
    )
    description = models.TextField(
        verbose_name='岗位描述'
    )
    requirements = models.TextField(
        verbose_name='任职要求'
    )
    num_positions = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='招聘人数'
    )
    num_filled = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='已录用人数'
    )
    work_hours_per_week = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='每周工时'
    )
    hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name='时薪（元/小时）'
    )
    start_date = models.DateField(
        verbose_name='开始日期'
    )
    end_date = models.DateField(
        verbose_name='结束日期'
    )
    application_deadline = models.DateTimeField(
        verbose_name='申请截止时间'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name='岗位状态'
    )
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='posted_positions',
        verbose_name='发布教师'
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
        db_table = 'position'
        verbose_name = '岗位'
        verbose_name_plural = '岗位'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['posted_by']),
            models.Index(fields=['course_code']),
            models.Index(fields=['application_deadline']),
        ]
    
    def __str__(self):
        return f'{self.title} ({self.course_name})'
    
    def is_full(self):
        """判断岗位是否已招满"""
        return self.num_filled >= self.num_positions
    
    def is_open(self):
        """判断岗位是否开放申请"""
        return self.status == 'open'
    
    def save(self, *args, **kwargs):
        """重写save方法，自动更新状态"""
        # 如果已招满，自动更新状态为filled
        if self.num_filled >= self.num_positions and self.status == 'open':
            self.status = 'filled'
        super().save(*args, **kwargs)
