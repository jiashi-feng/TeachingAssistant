"""
学生助教管理平台 - 申请流程模块Admin配置
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """申请记录管理"""
    
    list_display = [
        'application_id', 'get_applicant_name', 'get_position_title',
        'status_colored', 'applied_at', 'reviewed_by', 'reviewed_at'
    ]
    list_filter = ['status', 'applied_at', 'reviewed_at', 'position']
    search_fields = [
        'applicant__real_name', 'applicant__username',
        'position__title', 'position__course_name'
    ]
    ordering = ['-applied_at']
    date_hierarchy = 'applied_at'
    
    # 批量操作
    actions = ['batch_approve', 'batch_reject']
    
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
    
    def status_colored(self, obj):
        """彩色状态标签"""
        status_colors = {
            'pending': ('#e6a23c', '待审核'),
            'reviewing': ('#409eff', '审核中'),
            'accepted': ('#67c23a', '已通过'),
            'rejected': ('#f56c6c', '已拒绝'),
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
        """批量通过申请"""
        updated = queryset.update(
            status='accepted',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'成功通过 {updated} 个申请')
    batch_approve.short_description = '✓ 批量通过选中的申请'
    
    def batch_reject(self, request, queryset):
        """批量拒绝申请"""
        updated = queryset.update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'成功拒绝 {updated} 个申请')
    batch_reject.short_description = '✗ 批量拒绝选中的申请'
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时，申请时间只读"""
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['position', 'applicant', 'applied_at']
        return self.readonly_fields
