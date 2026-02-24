"""
学生助教管理平台 - 权限控制类

基于用户角色的权限控制（RBAC - Role-Based Access Control）
"""

from rest_framework import permissions
from .models import UserRole, Student


class IsStudent(permissions.BasePermission):
    """
    学生权限：只允许拥有 student 角色的用户访问
    """
    message = '只有学生可以访问此接口'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 检查用户是否有student角色
        return UserRole.objects.filter(
            user=request.user,
            role__role_code='student'
        ).exists()


class IsTA(permissions.BasePermission):
    """
    助教权限：只允许拥有助教身份的学生访问
    通过检查Student表的is_ta字段判断
    """
    message = '只有助教可以访问此接口'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 检查用户是否为助教
        try:
            student = Student.objects.get(user=request.user)
            return student.is_ta
        except Student.DoesNotExist:
            return False


class IsFaculty(permissions.BasePermission):
    """
    教师权限：只允许拥有 faculty 角色的用户访问
    """
    message = '只有教师可以访问此接口'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 检查用户是否有faculty角色
        return UserRole.objects.filter(
            user=request.user,
            role__role_code='faculty'
        ).exists()


class IsAdministrator(permissions.BasePermission):
    """
    管理员权限：拥有 administrator 角色，或 Django 后台用户（is_staff）均可访问
    这样从 Django Admin 点击导出/趋势链接时，Session 登录的 staff 用户也能通过
    """
    message = '只有管理员可以访问此接口'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if getattr(request.user, 'is_staff', False):
            return True
        return UserRole.objects.filter(
            user=request.user,
            role__role_code='administrator'
        ).exists()


class IsStudentOrTA(permissions.BasePermission):
    """
    学生或助教权限：允许拥有student角色的用户访问（包括助教）
    """
    message = '只有学生或助教可以访问此接口'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return UserRole.objects.filter(
            user=request.user,
            role__role_code='student'
        ).exists()


class HasPermission(permissions.BasePermission):
    """
    自定义权限检查：检查用户是否拥有特定权限
    
    使用方法：
        permission_classes = [HasPermission]
        permission_required = 'view_position'  # 在视图中定义
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 从视图获取所需权限
        required_permission = getattr(view, 'permission_required', None)
        if not required_permission:
            return True  # 如果没有定义权限要求，默认允许
        
        # 检查用户是否拥有该权限
        return request.user.has_permission(required_permission)


class IsOwner(permissions.BasePermission):
    """
    对象所有者权限：只允许对象的所有者访问
    要求对象有 'user' 或 'created_by' 字段
    """
    message = '只有对象所有者可以执行此操作'
    
    def has_object_permission(self, request, view, obj):
        # 检查对象是否有user字段
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # 检查对象是否有created_by字段
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        # 检查对象是否有applicant字段（申请记录）
        elif hasattr(obj, 'applicant'):
            return obj.applicant == request.user
        # 检查对象是否有posted_by字段（岗位）
        elif hasattr(obj, 'posted_by'):
            return obj.posted_by == request.user
        
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限：对象所有者可以编辑，其他人只读
    """
    message = '只有对象所有者可以修改'
    
    def has_object_permission(self, request, view, obj):
        # 读权限允许任何已登录用户
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        # 写权限只允许对象所有者
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        elif hasattr(obj, 'posted_by'):
            return obj.posted_by == request.user
        
        return False


class IsFacultyOrAdmin(permissions.BasePermission):
    """
    教师或管理员权限：允许教师和管理员访问
    """
    message = '只有教师或管理员可以访问此接口'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return UserRole.objects.filter(
            user=request.user,
            role__role_code__in=['faculty', 'administrator']
        ).exists()


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    管理员或只读权限：管理员可以修改，其他人只读
    """
    message = '只有管理员可以修改'
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 读权限允许所有已登录用户
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # 写权限只允许管理员
        return UserRole.objects.filter(
            user=request.user,
            role__role_code='administrator'
        ).exists()
