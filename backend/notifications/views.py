"""
学生助教管理平台 - 通知系统模块视图
"""

from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from django.utils import timezone
from django.db import transaction
from .models import Notification
from .serializers import NotificationSerializer, NotificationListSerializer


class NotificationList(generics.ListAPIView):
    """
    通知列表
    GET /api/notifications/
    支持筛选：is_read, category, notification_type
    支持排序：-created_at
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_read', 'category', 'notification_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """获取当前用户的通知列表"""
        queryset = Notification.objects.filter(
            recipient=self.request.user
        ).select_related('sender')
        
        # 过滤过期通知（可选，根据需求决定是否显示过期通知）
        # queryset = queryset.filter(
        #     Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())
        # )
        
        return queryset


class NotificationDetail(generics.RetrieveAPIView):
    """
    通知详情
    GET /api/notifications/{notification_id}/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    lookup_field = 'notification_id'
    
    def get_queryset(self):
        """只允许查看自己的通知"""
        return Notification.objects.filter(
            recipient=self.request.user
        ).select_related('sender')
    
    def retrieve(self, request, *args, **kwargs):
        """获取详情时自动标记为已读"""
        instance = self.get_object()
        if not instance.is_read:
            instance.mark_as_read()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class MarkAsRead(APIView):
    """
    标记通知为已读
    POST /api/notifications/{notification_id}/read/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, notification_id):
        """标记单个通知为已读"""
        notification = Notification.objects.filter(
            notification_id=notification_id,
            recipient=request.user
        ).first()
        
        if not notification:
            return Response(
                {'detail': '通知不存在或无权访问'},
                status=404
            )
        
        if not notification.is_read:
            notification.mark_as_read()
        
        return Response({
            'notification_id': notification.notification_id,
            'is_read': notification.is_read,
            'read_at': notification.read_at,
        })


class MarkAllAsRead(APIView):
    """
    全部标记为已读
    POST /api/notifications/read-all/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """将当前用户的所有未读通知标记为已读"""
        now = timezone.now()
        updated_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=now
        )
        
        return Response({
            'updated_count': updated_count,
            'message': f'已标记 {updated_count} 条通知为已读',
        })


class UnreadCount(APIView):
    """
    未读通知数量
    GET /api/notifications/unread-count/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """获取当前用户的未读通知数量"""
        count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        
        # 按分类统计未读数量
        category_counts = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).values('category').annotate(
            count=Count('notification_id')
        )
        
        category_dict = {item['category']: item['count'] for item in category_counts}
        
        return Response({
            'total_unread': count,
            'by_category': {
                'system': category_dict.get('system', 0),
                'application': category_dict.get('application', 0),
                'timesheet': category_dict.get('timesheet', 0),
                'salary': category_dict.get('salary', 0),
            },
        })
