"""
学生助教管理平台 - 通知系统模块Admin配置
"""

from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """通知管理"""
    
    list_display = [
        'notification_id', 'get_recipient_name', 'notification_type',
        'category', 'title', 'priority',
        'is_read', 'created_at'
    ]
    list_filter = [
        'category', 'notification_type', 'priority',
        'is_read', 'created_at'
    ]
    search_fields = [
        'recipient__real_name', 'recipient__username',
        'sender__real_name', 'title', 'message'
    ]
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('接收者信息', {
            'fields': ('recipient', 'sender')
        }),
        ('通知内容', {
            'fields': (
                'notification_type', 'category', 'priority',
                'title', 'message'
            )
        }),
        ('关联信息', {
            'fields': ('related_model', 'related_object_id')
        }),
        ('状态', {
            'fields': ('is_read', 'read_at', 'expires_at')
        }),
    )
    
    readonly_fields = ['created_at', 'read_at']
    
    def get_recipient_name(self, obj):
        return obj.recipient.real_name
    get_recipient_name.short_description = '接收人'
    get_recipient_name.admin_order_field = 'recipient__real_name'
    
    def get_readonly_fields(self, request, obj=None):
        """编辑时，创建时间和接收人只读"""
        if obj:  # 编辑现有对象
            return self.readonly_fields + ['recipient', 'created_at']
        return self.readonly_fields
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """批量标记为已读"""
        from django.utils import timezone
        updated = queryset.filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )
        self.message_user(request, f'成功标记 {updated} 条通知为已读')
    mark_as_read.short_description = '标记为已读'
    
    def mark_as_unread(self, request, queryset):
        """批量标记为未读"""
        updated = queryset.filter(is_read=True).update(
            is_read=False,
            read_at=None
        )
        self.message_user(request, f'成功标记 {updated} 条通知为未读')
    mark_as_unread.short_description = '标记为未读'
