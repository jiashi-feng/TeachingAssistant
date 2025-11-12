"""
学生助教管理平台 - 通知系统模块URL配置
"""

from django.urls import path
from .views import (
    NotificationList,
    NotificationDetail,
    MarkAsRead,
    MarkAllAsRead,
    UnreadCount,
)

app_name = 'notifications'

urlpatterns = [
    # 通知列表
    path('api/notifications/', NotificationList.as_view(), name='notification-list'),
    
    # 通知详情（查看时自动标记为已读）
    path('api/notifications/<int:notification_id>/', NotificationDetail.as_view(), name='notification-detail'),
    
    # 标记已读
    path('api/notifications/<int:notification_id>/read/', MarkAsRead.as_view(), name='mark-as-read'),
    
    # 全部标记为已读
    path('api/notifications/read-all/', MarkAllAsRead.as_view(), name='mark-all-as-read'),
    
    # 未读数量
    path('api/notifications/unread-count/', UnreadCount.as_view(), name='unread-count'),
]

