"""
学生助教管理平台 - 工时管理模块模型
包含：Timesheet（工时表）、Salary（薪酬记录表）
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from recruitment.models import Position


class Timesheet(models.Model):
    """工时表 - 记录助教的工作时间"""
    
    # 审核状态选择
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已批准'),
        ('rejected', '已驳回'),
    ]
    
    timesheet_id = models.AutoField(
        primary_key=True,
        verbose_name='工时表ID'
    )
    ta = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='timesheets',
        verbose_name='助教'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='timesheets',
        verbose_name='岗位'
    )
    month = models.DateField(
        verbose_name='工作月份',
        help_text='存储月初日期，如: 2025-03-01'
    )
    hours_worked = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(744)  # 31天 × 24小时
        ],
        verbose_name='工作小时数'
    )
    work_description = models.TextField(
        verbose_name='工作描述'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='审核状态'
    )
    submitted_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='提交时间'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_timesheets',
        verbose_name='审核教师'
    )
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='审核时间'
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
        db_table = 'timesheet'
        verbose_name = '工时表'
        verbose_name_plural = '工时表'
        # 唯一约束：同一助教同一岗位同一月份只能提交一次工时表
        unique_together = [['ta', 'position', 'month']]
        ordering = ['-month', '-submitted_at']
        indexes = [
            models.Index(fields=['ta']),
            models.Index(fields=['position']),
            models.Index(fields=['status']),
            models.Index(fields=['month']),
        ]
    
    def __str__(self):
        return f'{self.ta.real_name} - {self.position.title} - {self.month.strftime("%Y年%m月")}'
    
    def is_pending(self):
        """判断工时表是否待审核"""
        return self.status == 'pending'
    
    def is_approved(self):
        """判断工时表是否已批准"""
        return self.status == 'approved'
    
    def calculate_salary(self):
        """计算薪酬金额"""
        return float(self.hours_worked) * float(self.position.hourly_rate)


class Salary(models.Model):
    """薪酬记录表 - 记录助教的薪酬信息，由管理员根据已批准的工时生成"""
    
    # 支付状态选择
    PAYMENT_STATUS_CHOICES = [
        ('pending', '待支付'),
        ('paid', '已支付'),
    ]
    
    salary_id = models.AutoField(
        primary_key=True,
        verbose_name='薪酬ID'
    )
    timesheet = models.OneToOneField(
        Timesheet,
        on_delete=models.CASCADE,
        related_name='salary',
        verbose_name='关联工时表'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='薪酬金额（元）'
    )
    calculation_details = models.JSONField(
        null=True,
        blank=True,
        verbose_name='计算明细',
        help_text='JSON格式存储计算过程，如: {"hours":40.5, "rate":50, "formula":"40.5×50"}'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name='支付状态'
    )
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='generated_salaries',
        verbose_name='报表生成人（管理员）'
    )
    generated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='报表生成时间'
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='支付时间'
    )
    payment_method = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='支付方式',
        help_text='如: 银行转账, 支付宝'
    )
    transaction_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='交易流水号'
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
        db_table = 'salary'
        verbose_name = '薪酬记录'
        verbose_name_plural = '薪酬记录'
        ordering = ['-generated_at']
        indexes = [
            models.Index(fields=['payment_status']),
            models.Index(fields=['generated_by']),
            models.Index(fields=['generated_at']),
        ]
    
    def __str__(self):
        return f'{self.timesheet.ta.real_name} - {self.timesheet.month.strftime("%Y年%m月")} - ¥{self.amount}'
    
    def is_paid(self):
        """判断薪酬是否已支付"""
        return self.payment_status == 'paid'
    
    def save(self, *args, **kwargs):
        """重写save方法，自动计算薪酬金额和计算明细"""
        if not self.amount:
            # 自动计算薪酬金额
            self.amount = self.timesheet.calculate_salary()
        
        if not self.calculation_details:
            # 自动生成计算明细
            self.calculation_details = {
                'hours': float(self.timesheet.hours_worked),
                'rate': float(self.timesheet.position.hourly_rate),
                'formula': f'{self.timesheet.hours_worked} × {self.timesheet.position.hourly_rate}'
            }
        
        super().save(*args, **kwargs)
