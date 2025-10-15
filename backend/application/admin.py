"""
学生助教管理平台 - 申请流程模块Admin配置
"""

from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """申请记录管理"""
    
    list_display = [
        'application_id', 'get_applicant_name', 'get_position_title',
        'status', 'applied_at', 'reviewed_by', 'reviewed_at'
    ]
    list_filter = ['status', 'applied_at', 'reviewed_at', 'position']
    search_fields = [
        'applicant__real_name', 'applicant__username',
        'position__title', 'position__course_name'
    ]
    ordering = ['-applied_at']
    date_hierarchy = 'applied_at'
    
    fieldsets = (
        ('申请信息', {
            'fields': ('position', 'applicant', 'status', 'resume')
        }),
        ('审核信息', {
            'fields': ('reviewed_by', 'reviewed_at', 'review_notes')
        }),
    )
    
    readonly_fields = ['applied_at', 'created_at', 'updated_at']
    
    def get_applicant_name(self, obj):
        return obj.applicant.real_name
    get_applicant_name.short_description = '申请人'
    get_applicant_name.admin_order_field = 'applicant__real_name'
    
    def get_position_title(self, obj):
        return obj.position.title
    get_position_title.short_description = '岗位'
    get_position_title.admin_order_field = 'position__title'
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时，申请时间只读"""
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['position', 'applicant', 'applied_at']
        return self.readonly_fields
