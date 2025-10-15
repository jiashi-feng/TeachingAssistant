"""
学生助教管理平台 - 招募管理模块Admin配置
"""

from django.contrib import admin
from .models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    """岗位管理"""
    
    list_display = [
        'position_id', 'title', 'course_name', 'course_code',
        'num_positions', 'num_filled', 'hourly_rate',
        'status', 'application_deadline', 'posted_by'
    ]
    list_filter = ['status', 'posted_by', 'created_at', 'application_deadline']
    search_fields = ['title', 'course_name', 'course_code', 'posted_by__real_name']
    ordering = ['-created_at']
    date_hierarchy = 'application_deadline'
    
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
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时，已录用人数只读"""
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['num_filled']
        return self.readonly_fields
