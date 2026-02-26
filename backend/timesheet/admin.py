"""
学生助教管理平台 - 工时管理模块Admin配置
"""

import json
import uuid

from django import forms
from django.urls import path, reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Timesheet, Salary


@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    """工时表管理"""
    
    list_display = [
        'timesheet_id', 'get_ta_name', 'get_position_title',
        'month', 'hours_worked', 'status_colored',
        'submitted_at', 'reviewed_by'
    ]
    list_filter = ['status', 'month', 'submitted_at', 'reviewed_at']
    search_fields = [
        'ta__real_name', 'ta__username',
        'position__title', 'position__course_name'
    ]
    ordering = ['-month', '-submitted_at']
    date_hierarchy = 'month'
    
    # 批量操作
    actions = ['batch_approve', 'batch_reject']
    
    fieldsets = (
        ('工时信息', {
            'fields': ('ta', 'position', 'month', 'hours_worked', 'work_description')
        }),
        ('审核信息', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'review_notes')
        }),
    )
    
    readonly_fields = ['submitted_at', 'created_at', 'updated_at']
    
    def get_ta_name(self, obj):
        return obj.ta.real_name
    get_ta_name.short_description = '助教'
    get_ta_name.admin_order_field = 'ta__real_name'
    
    def get_position_title(self, obj):
        return obj.position.title
    get_position_title.short_description = '岗位'
    get_position_title.admin_order_field = 'position__title'
    
    def status_colored(self, obj):
        """彩色状态标签"""
        status_colors = {
            'pending': ('#e6a23c', '待审核'),
            'approved': ('#67c23a', '已批准'),
            'rejected': ('#f56c6c', '已驳回'),
        }
        color, label = status_colors.get(obj.status, ('#909399', obj.get_status_display()))
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 12px; font-weight: 500;">{}</span>',
            color, label
        )
    status_colored.short_description = '状态'
    status_colored.admin_order_field = 'status'
    
    def batch_approve(self, request, queryset):
        """批量批准工时"""
        updated = queryset.update(
            status='approved',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'成功批准 {updated} 个工时表')
    batch_approve.short_description = '✓ 批量批准选中的工时'
    
    def batch_reject(self, request, queryset):
        """批量驳回工时"""
        updated = queryset.update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'成功驳回 {updated} 个工时表')
    batch_reject.short_description = '✗ 批量驳回选中的工时'
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时，部分字段只读"""
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['ta', 'position', 'month', 'submitted_at']
        return self.readonly_fields


class SalaryAdminForm(forms.ModelForm):
    """薪酬记录表单：自动计算金额与明细"""

    class Meta:
        model = Salary
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 支付方式使用下拉框
        self.fields['payment_method'] = forms.ChoiceField(
            choices=[('', '---------')] + list(Salary.PAYMENT_METHOD_CHOICES),
            required=False,
            label='支付方式',
        )

        # 薪酬金额、计算明细由系统计算，设为只读
        self.fields['amount'].required = False
        self.fields['amount'].widget.attrs['readonly'] = True
        self.fields['calculation_details'].required = False
        self.fields['calculation_details'].widget = forms.Textarea(
            attrs={
                'readonly': True,
                'rows': 5,
                'style': 'font-family: monospace;',
            }
        )
        self.fields['calculation_details'].initial = self.fields['calculation_details'].initial or ''
        self.fields['amount'].initial = self.fields['amount'].initial or ''

        # 动态计算薪酬的接口地址（供前端JS使用）
        base_calc_url = reverse('admin:timesheet_salary_calc', args=[0]).rsplit('0/', 1)[0]
        self.fields['timesheet'].widget.attrs['data-calc-url'] = base_calc_url

        # 编辑已有记录时，展示已保存的计算明细
        if self.instance and self.instance.pk:
            self.fields['amount'].initial = self.instance.amount
            if self.instance.calculation_details:
                self.fields['calculation_details'].initial = json.dumps(
                    self.instance.calculation_details,
                    ensure_ascii=False,
                    indent=2,
                )

    def clean(self):
        cleaned_data = super().clean()
        timesheet = cleaned_data.get('timesheet')

        if not timesheet:
            return cleaned_data

        # 仅允许为已批准的工时生成薪酬
        if timesheet.status != 'approved':
            raise forms.ValidationError('只能为已批准的工时表生成薪酬记录。')

        amount = timesheet.calculate_salary()
        details = {
            '工时（小时）': float(timesheet.hours_worked),
            '时薪（元/小时）': float(timesheet.position.hourly_rate),
            '计算公式': f'{timesheet.hours_worked} × {timesheet.position.hourly_rate}',
        }

        cleaned_data['amount'] = amount
        cleaned_data['calculation_details'] = details

        # 更新表单显示
        self.fields['amount'].initial = amount
        self.fields['calculation_details'].initial = json.dumps(
            details,
            ensure_ascii=False,
            indent=2,
        )

        return cleaned_data


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    """薪酬记录管理"""
    form = SalaryAdminForm
    
    class Media:
        js = ('timesheet/js/salary_admin.js',)

    list_display = [
        'salary_id', 'get_ta_name', 'get_month',
        'amount', 'payment_status',
        'generated_by', 'generated_at', 'paid_at'
    ]
    list_filter = ['payment_status', 'generated_at', 'paid_at']
    search_fields = [
        'timesheet__ta__real_name',
        'timesheet__ta__username',
        'generated_by__real_name'
    ]
    ordering = ['-generated_at']
    date_hierarchy = 'generated_at'
    
    fieldsets = (
        ('关联信息', {
            'fields': ('timesheet',)
        }),
        ('薪酬信息', {
            'fields': ('amount', 'calculation_details', 'payment_status')
        }),
        ('支付信息', {
            'fields': ('payment_method', 'transaction_id', 'paid_at')
        }),
        ('系统信息', {
            'classes': ('collapse',),
            'fields': ('generated_by', 'generated_at', 'created_at', 'updated_at')
        }),
    )
    
    readonly_fields = ['generated_by', 'generated_at', 'created_at', 'updated_at']
    
    def get_ta_name(self, obj):
        return obj.timesheet.ta.real_name
    get_ta_name.short_description = '助教'
    
    def get_month(self, obj):
        # 使用 f-string 避免 Windows locale 编码问题
        return f"{obj.timesheet.month.year}年{obj.timesheet.month.month:02d}月"
    get_month.short_description = '月份'
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时，部分字段只读"""
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['timesheet', 'amount', 'calculation_details']
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        """保存时自动写入金额、计算明细与生成管理员"""
        if not obj.generated_by_id:
            obj.generated_by = request.user

        if form.cleaned_data.get('amount') is not None:
            obj.amount = form.cleaned_data['amount']
        if form.cleaned_data.get('calculation_details') is not None:
            obj.calculation_details = form.cleaned_data['calculation_details']

        if not obj.transaction_id:
            obj.transaction_id = uuid.uuid4().hex.upper()

        super().save_model(request, obj, form, change)

    # ===== 自定义接口：根据工时计算薪酬 =====
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'calc-timesheet/<int:timesheet_id>/',
                self.admin_site.admin_view(self.calc_timesheet),
                name='timesheet_salary_calc'
            ),
        ]
        return custom_urls + urls

    def calc_timesheet(self, request, timesheet_id):
        """根据工时ID计算薪酬（AJAX调用）"""
        timesheet = get_object_or_404(
            Timesheet.objects.select_related('position', 'ta'),
            timesheet_id=timesheet_id
        )

        if timesheet.status != 'approved':
            return JsonResponse(
                {'error': '该工时尚未批准，无法生成薪酬记录。'},
                status=400
            )

        amount = timesheet.calculate_salary()
        details = {
            '工时（小时）': float(timesheet.hours_worked),
            '时薪（元/小时）': float(timesheet.position.hourly_rate),
            '计算公式': f'{timesheet.hours_worked} × {timesheet.position.hourly_rate}',
        }
        return JsonResponse({
            'amount': str(amount),
            'details': details,
            'timesheet': {
                'id': timesheet.timesheet_id,
                'ta': timesheet.ta.real_name,
                'position': timesheet.position.title,
            }
        })
