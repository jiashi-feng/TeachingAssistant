"""
学生助教管理平台 - 用户认证模块Admin配置
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Role, Permission, UserRole, RolePermission, Student, Faculty, Administrator


# ==============================================================================
# 用户Admin
# ==============================================================================

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    
    list_display = ['user_id', 'username', 'real_name', 'email', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['user_id', 'username', 'real_name', 'email', 'phone']
    ordering = ['-date_joined']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('user_id', 'username', 'email', 'password_status')
        }),
        ('个人信息', {
            'fields': ('real_name', 'phone', 'avatar')
        }),
        ('权限', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('重要日期', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        ('创建新用户', {
            'classes': ('wide',),
            'fields': ('user_id', 'username', 'email', 'real_name', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login', 'created_at', 'updated_at', 'password_status']

    def password_status(self, obj):
        """简单的密码状态显示方法"""
        if obj and obj.password:
            return '●●●●●●●● (密码已安全设置)'
        return '未设置密码'
    password_status.short_description = '密码状态'

    def get_fieldsets(self, request, obj=None):
        """动态生成fieldsets，只在编辑时显示密码状态"""
        if obj:  # 编辑现有用户
            return (
                ('基本信息', {
                    'fields': ('user_id', 'username', 'email', 'password_status')
                }),
                ('个人信息', {
                    'fields': ('real_name', 'phone', 'avatar')
                }),
                ('权限', {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
                }),
                ('重要日期', {
                    'fields': ('last_login', 'date_joined')
                }),
            )
        else:  # 创建新用户
            return super().get_fieldsets(request, obj)

    def get_fields(self, request, obj=None):
        """获取字段列表"""
        if obj:  # 编辑现有用户
            return ['user_id', 'username', 'email', 'password_status', 'real_name', 'phone', 'avatar', 
                   'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 
                   'last_login', 'date_joined']
        else:  # 创建新用户
            return super().get_fields(request, obj)


# ==============================================================================
# 角色与权限Admin
# ==============================================================================

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """角色管理"""
    
    list_display = ['role_id', 'role_code', 'role_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['role_code', 'role_name']
    ordering = ['role_id']
    
    fieldsets = (
        ('角色信息', {
            'fields': ('role_code', 'role_name', 'description')
        }),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """权限管理"""
    
    list_display = ['permission_id', 'permission_code', 'permission_name', 'module', 'created_at']
    list_filter = ['module', 'created_at']
    search_fields = ['permission_code', 'permission_name']
    ordering = ['module', 'permission_code']
    
    fieldsets = (
        ('权限信息', {
            'fields': ('permission_code', 'permission_name', 'module', 'description')
        }),
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """用户角色关联管理"""
    
    list_display = ['user', 'role', 'is_primary', 'assigned_at', 'assigned_by']
    list_filter = ['role', 'is_primary', 'assigned_at']
    search_fields = ['user__username', 'user__real_name', 'role__role_name']
    ordering = ['-assigned_at']
    
    fieldsets = (
        ('关联信息', {
            'fields': ('user', 'role', 'is_primary', 'assigned_by')
        }),
    )
    
    readonly_fields = ['assigned_at', 'created_at']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """角色权限关联管理"""
    
    list_display = ['role', 'permission', 'granted_at']
    list_filter = ['role', 'granted_at']
    search_fields = ['role__role_name', 'permission__permission_name']
    ordering = ['role', 'permission']
    
    fieldsets = (
        ('关联信息', {
            'fields': ('role', 'permission')
        }),
    )
    
    readonly_fields = ['granted_at', 'created_at']


# ==============================================================================
# 学生/教师/管理员信息Admin
# ==============================================================================

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """学生信息管理"""
    
    list_display = ['student_id', 'get_real_name', 'department', 'major', 'grade', 'is_ta', 'ta_since']
    list_filter = ['department', 'grade', 'is_ta', 'created_at']
    search_fields = ['student_id', 'user__real_name', 'user__username', 'department', 'major']
    ordering = ['-grade', 'student_id']
    
    fieldsets = (
        ('关联用户', {
            'fields': ('user',)
        }),
        ('学生信息', {
            'fields': ('student_id', 'department', 'major', 'grade', 'class_name')
        }),
        ('助教状态', {
            'fields': ('is_ta', 'ta_since')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_real_name(self, obj):
        return obj.user.real_name
    get_real_name.short_description = '姓名'
    get_real_name.admin_order_field = 'user__real_name'


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    """教师信息管理"""
    
    list_display = ['faculty_id', 'get_real_name', 'department', 'title', 'office_location']
    list_filter = ['department', 'title', 'created_at']
    search_fields = ['faculty_id', 'user__real_name', 'user__username', 'department']
    ordering = ['faculty_id']
    
    fieldsets = (
        ('关联用户', {
            'fields': ('user',)
        }),
        ('教师信息', {
            'fields': ('faculty_id', 'department', 'title', 'office_location', 'research_area')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_real_name(self, obj):
        return obj.user.real_name
    get_real_name.short_description = '姓名'
    get_real_name.admin_order_field = 'user__real_name'


@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    """管理员信息管理"""
    
    list_display = ['admin_id', 'get_real_name', 'department', 'position']
    list_filter = ['department', 'created_at']
    search_fields = ['admin_id', 'user__real_name', 'user__username', 'department']
    ordering = ['admin_id']
    
    fieldsets = (
        ('关联用户', {
            'fields': ('user',)
        }),
        ('管理员信息', {
            'fields': ('admin_id', 'department', 'position')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_real_name(self, obj):
        return obj.user.real_name
    get_real_name.short_description = '姓名'
    get_real_name.admin_order_field = 'user__real_name'