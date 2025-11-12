"""
学生助教管理平台 - 通知系统模块序列化器
"""

from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """通知序列化器"""
    sender_name = serializers.CharField(
        source='sender.real_name',
        read_only=True,
        allow_null=True
    )
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )
    priority_display = serializers.CharField(
        source='get_priority_display',
        read_only=True
    )
    
    class Meta:
        model = Notification
        fields = [
            'notification_id',
            'recipient',
            'sender',
            'sender_name',
            'notification_type',
            'notification_type_display',
            'category',
            'category_display',
            'title',
            'message',
            'priority',
            'priority_display',
            'is_read',
            'read_at',
            'related_model',
            'related_object_id',
            'expires_at',
            'created_at',
        ]
        read_only_fields = [
            'notification_id',
            'recipient',
            'sender',
            'notification_type',
            'category',
            'title',
            'message',
            'priority',
            'is_read',
            'read_at',
            'related_model',
            'related_object_id',
            'expires_at',
            'created_at',
        ]


class NotificationListSerializer(serializers.ModelSerializer):
    """通知列表序列化器（简化版）"""
    sender_name = serializers.CharField(
        source='sender.real_name',
        read_only=True,
        allow_null=True
    )
    notification_type_display = serializers.CharField(
        source='get_notification_type_display',
        read_only=True
    )
    category_display = serializers.CharField(
        source='get_category_display',
        read_only=True
    )
    
    class Meta:
        model = Notification
        fields = [
            'notification_id',
            'sender_name',
            'notification_type',
            'notification_type_display',
            'category',
            'category_display',
            'title',
            'message',
            'is_read',
            'read_at',
            'related_model',
            'related_object_id',
            'created_at',
        ]

