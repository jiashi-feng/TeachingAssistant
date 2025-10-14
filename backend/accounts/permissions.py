"""
权限控制类

基于用户角色的权限控制（RBAC - Role-Based Access Control）
"""

from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """
    学生权限：只允许角色为 student 或 ta 的用户访问
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
               request.user.role in ['student', 'ta']


class IsTA(permissions.BasePermission):
    """
    助教权限：只允许角色为 ta 的用户访问
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
               request.user.role == 'ta'


class IsFaculty(permissions.BasePermission):
    """
    教师权限：只允许角色为 faculty 的用户访问
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
               request.user.role == 'faculty'


class IsAdmin(permissions.BasePermission):
    """
    管理员权限：只允许角色为 admin 的用户访问
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and \
               request.user.role == 'admin'


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限：对象所有者可以编辑，其他人只读
    """
    def has_object_permission(self, request, view, obj):
        # 读权限允许任何请求
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 写权限只允许对象所有者
        return obj.user == request.user

