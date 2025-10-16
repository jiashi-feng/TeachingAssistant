"""
学生助教管理平台 - 招募管理模块Admin配置
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """岗位管理"""
    
    list_display = [
        'position_id', 'title', 'course_name', 'course_code',
        'num_positions', 'num_filled', 'hourly_rate',
        'status_colored', 'application_deadline', 'posted_by'
    ]
    list_filter = ['status', 'posted_by', 'created_at', 'application_deadline']
    search_fields = ['title', 'course_name', 'course_code', 'posted_by__real_name']
    ordering = ['-created_at']
    date_hierarchy = 'application_deadline'
    
    # 批量操作
    actions = ['batch_close', 'batch_reopen']
    
    fieldsets = (
        ('岗位基本信息', {
            'fields': ('title', 'course_name', 'course_code', 'posted_by')
        }),
        ('岗位描述', {
            'fields': ('description', 'requirements')
        }),
        ('招聘信息', {
            'fields': (
                ('num_positions', 'num_filled'),
                'work_hours_per_week',
                'hourly_rate'
            )
        }),
        ('时间安排', {
            'fields': (
                ('start_date', 'end_date'),
                'application_deadline'
            )
        }),
        ('状态', {
            'fields': ('status',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def status_colored(self, obj):
        """彩色状态标签"""
        status_colors = {
            'open': ('#67c23a', '开放中'),
            'closed': ('#909399', '已关闭'),
            'filled': ('#409eff', '已满员'),
        }
        color, label = status_colors.get(obj.status, ('#909399', obj.get_status_display()))
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; '
            'border-radius: 12px; font-size: 12px; font-weight: 500;">{}</span>',
            color, label
        )
    status_colored.short_description = '状态'
    status_colored.admin_order_field = 'status'
    
    def batch_close(self, request, queryset):
        """批量关闭岗位"""
        updated = queryset.update(status='closed')
        self.message_user(request, f'成功关闭 {updated} 个岗位')
    batch_close.short_description = '关闭选中的岗位'
    
    def batch_reopen(self, request, queryset):
        """批量重新开放岗位"""
        updated = queryset.update(status='open')
        self.message_user(request, f'成功重新开放 {updated} 个岗位')
    batch_reopen.short_description = '重新开放选中的岗位'
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时，已录用人数只读"""
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['num_filled']
        return self.readonly_fields
