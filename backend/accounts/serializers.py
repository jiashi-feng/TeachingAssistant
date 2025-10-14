"""
序列化器 (Serializers)

用于将Django模型转换为JSON格式，以及验证前端提交的数据
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器 - 用于返回用户信息（不包含密码）
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'student_id', 
                  'phone', 'department', 'avatar', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    """
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 
                  'role', 'student_id', 'phone', 'department']
    
    def validate(self, data):
        """验证密码是否一致"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("两次输入的密码不一致")
        return data
    
    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # 密码加密
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    用户登录序列化器
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    """
    修改密码序列化器
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
    new_password_confirm = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """验证新密码是否一致"""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("两次输入的新密码不一致")
        return data

