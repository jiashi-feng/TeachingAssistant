"""
学生助教管理平台 - 工时管理模块Admin配置
"""

from django.contrib import admin
from .models import Timesheet, Salary


@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    """工时表管理"""
    
    list_display = [
        'timesheet_id', 'get_ta_name', 'get_position_title',
        'month', 'hours_worked', 'status',
        'submitted_at', 'reviewed_by'
    ]
    list_filter = ['status', 'month', 'submitted_at', 'reviewed_at']
    search_fields = [
        'ta__real_name', 'ta__username',
        'position__title', 'position__course_name'
    ]
    ordering = ['-month', '-submitted_at']
    date_hierarchy = 'month'
    
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
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时，部分字段只读"""
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['ta', 'position', 'month', 'submitted_at']
        return self.readonly_fields


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    """薪酬记录管理"""
    
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
            'fields': ('timesheet', 'generated_by')
        }),
        ('薪酬信息', {
            'fields': ('amount', 'calculation_details', 'payment_status')
        }),
        ('支付信息', {
            'fields': ('payment_method', 'transaction_id', 'paid_at')
        }),
    )
    
    readonly_fields = ['generated_at', 'created_at', 'updated_at']
    
    def get_ta_name(self, obj):
        return obj.timesheet.ta.real_name
    get_ta_name.short_description = '助教'
    
    def get_month(self, obj):
        return obj.timesheet.month.strftime('%Y年%m月')
    get_month.short_description = '月份'
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时，部分字段只读"""
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['timesheet', 'generated_by', 'amount', 'calculation_details']
        return self.readonly_fields
