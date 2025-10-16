"""
学生助教管理平台 - 用户认证模块序列化器

用于将Django模型转换为JSON格式，以及验证前端提交的数据
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Role, Permission, UserRole, Student, Faculty, Administrator


# ==============================================================================
# 角色和权限序列化器
# ==============================================================================

class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    class Meta:
        model = Role
        fields = ['role_id', 'role_code', 'role_name', 'description']


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    class Meta:
        model = Permission
        fields = ['permission_id', 'permission_code', 'permission_name', 'module', 'description']


# ==============================================================================
# 扩展信息序列化器
# ==============================================================================

class StudentSerializer(serializers.ModelSerializer):
    """学生信息序列化器"""
    class Meta:
        model = Student
        fields = ['student_id', 'department', 'major', 'grade', 'class_name', 'is_ta', 'ta_since']
        read_only_fields = ['is_ta', 'ta_since']


class FacultySerializer(serializers.ModelSerializer):
    """教师信息序列化器"""
    class Meta:
        model = Faculty
        fields = ['faculty_id', 'department', 'title', 'office_location', 'research_area']


class AdministratorSerializer(serializers.ModelSerializer):
    """管理员信息序列化器"""
    class Meta:
        model = Administrator
        fields = ['admin_id', 'department', 'position']


# ==============================================================================
# 用户序列化器
# ==============================================================================

class UserSerializer(serializers.ModelSerializer):
    """
    用户基本信息序列化器 - 用于返回用户信息（不包含密码）
    """
    roles = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    primary_role = serializers.SerializerMethodField()
    
    # 扩展信息（根据角色动态返回）
    student_info = serializers.SerializerMethodField()
    faculty_info = serializers.SerializerMethodField()
    admin_info = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'real_name', 'phone', 'avatar',
            'is_active', 'date_joined', 'last_login', 'created_at',
            'roles', 'permissions', 'primary_role',
            'student_info', 'faculty_info', 'admin_info'
        ]
        read_only_fields = ['user_id', 'date_joined', 'last_login', 'created_at']
    
    def get_roles(self, obj):
        """获取用户的所有角色"""
        user_roles = UserRole.objects.filter(user=obj).select_related('role')
        return [
            {
                'role_id': ur.role.role_id,
                'role_code': ur.role.role_code,
                'role_name': ur.role.role_name,
                'is_primary': ur.is_primary
            }
            for ur in user_roles
        ]
    
    def get_permissions(self, obj):
        """获取用户的所有权限"""
        permissions = obj.get_all_permissions_list()
        return [p.permission_code for p in permissions]
    
    def get_primary_role(self, obj):
        """获取用户的主角色"""
        primary_role = obj.get_primary_role()
        if primary_role:
            return {
                'role_id': primary_role.role_id,
                'role_code': primary_role.role_code,
                'role_name': primary_role.role_name
            }
        return None
    
    def get_student_info(self, obj):
        """获取学生信息"""
        try:
            student = obj.student
            return StudentSerializer(student).data
        except Student.DoesNotExist:
            return None
    
    def get_faculty_info(self, obj):
        """获取教师信息"""
        try:
            faculty = obj.faculty
            return FacultySerializer(faculty).data
        except Faculty.DoesNotExist:
            return None
    
    def get_admin_info(self, obj):
        """获取管理员信息"""
        try:
            admin = obj.administrator
            return AdministratorSerializer(admin).data
        except Administrator.DoesNotExist:
            return None


class UserSimpleSerializer(serializers.ModelSerializer):
    """用户简化序列化器 - 用于列表展示"""
    primary_role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'real_name', 'email', 'primary_role', 'is_active']
    
    def get_primary_role(self, obj):
        """获取主角色名称"""
        primary_role = obj.get_primary_role()
        return primary_role.role_name if primary_role else None


# ==============================================================================
# 认证相关序列化器
# ==============================================================================

class RegisterSerializer(serializers.Serializer):
    """
    用户注册序列化器
    支持学生、教师、管理员三种角色的注册
    """
    # 基本信息
    user_id = serializers.CharField(
        max_length=20,
        help_text='用户ID: S+学号(学生) / F+工号(教师) / A+编号(管理员)'
    )
    username = serializers.CharField(
        max_length=150,
        min_length=3,
        help_text='用户名（登录用）'
    )
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    real_name = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=11, required=False, allow_blank=True)
    
    # 角色信息
    role_code = serializers.CharField(
        help_text='角色代码: student, faculty, administrator'
    )
    
    # 学生特有字段
    student_id = serializers.CharField(max_length=20, required=False)
    department = serializers.CharField(max_length=100, required=False)
    major = serializers.CharField(max_length=100, required=False)
    grade = serializers.IntegerField(required=False)
    class_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
    
    # 教师特有字段
    faculty_id = serializers.CharField(max_length=20, required=False)
    title = serializers.CharField(max_length=50, required=False)
    office_location = serializers.CharField(max_length=100, required=False, allow_blank=True)
    research_area = serializers.CharField(required=False, allow_blank=True)
    
    # 管理员特有字段
    admin_id = serializers.CharField(max_length=20, required=False)
    position = serializers.CharField(max_length=50, required=False)
    
    def validate_user_id(self, value):
        """验证user_id是否已存在"""
        if User.objects.filter(user_id=value).exists():
            raise serializers.ValidationError('该用户ID已被注册')
        return value
    
    def validate_username(self, value):
        """验证用户名是否已存在"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('该用户名已被注册')
        return value
    
    def validate_email(self, value):
        """验证邮箱是否已存在"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('该邮箱已被注册')
        return value
    
    def validate(self, data):
        """验证密码是否一致，并根据角色验证必填字段"""
        # 验证密码
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': '两次输入的密码不一致'})
        
        # 验证角色代码
        role_code = data.get('role_code')
        try:
            role = Role.objects.get(role_code=role_code)
        except Role.DoesNotExist:
            raise serializers.ValidationError({'role_code': f'角色代码 {role_code} 不存在'})
        
        # 根据角色验证必填字段
        if role_code == 'student':
            required_fields = ['student_id', 'department', 'major', 'grade']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f'学生注册时 {field} 为必填项'})
        
        elif role_code == 'faculty':
            required_fields = ['faculty_id', 'department', 'title']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f'教师注册时 {field} 为必填项'})
        
        elif role_code == 'administrator':
            required_fields = ['admin_id', 'department', 'position']
            for field in required_fields:
                if not data.get(field):
                    raise serializers.ValidationError({field: f'管理员注册时 {field} 为必填项'})
        
        return data
    
    def create(self, validated_data):
        """创建用户及相关信息"""
        # 提取基本信息
        user_id = validated_data['user_id']
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        real_name = validated_data['real_name']
        phone = validated_data.get('phone', '')
        role_code = validated_data['role_code']
        
        # 创建用户（传入user_id作为主键）
        user = User.objects.create_user(
            user_id=user_id,      # 主键必须在创建时传入
            username=username,
            email=email,
            password=password,
            real_name=real_name,  # 其他字段通过**extra_fields传入
            phone=phone
        )
        
        # 分配角色
        role = Role.objects.get(role_code=role_code)
        UserRole.objects.create(
            user=user,
            role=role,
            is_primary=True,
            assigned_by=None  # 自注册，无分配人
        )
        
        # 根据角色创建扩展信息
        if role_code == 'student':
            Student.objects.create(
                user=user,
                student_id=validated_data['student_id'],
                department=validated_data['department'],
                major=validated_data['major'],
                grade=validated_data['grade'],
                class_name=validated_data.get('class_name', '')
            )
        
        elif role_code == 'faculty':
            Faculty.objects.create(
                user=user,
                faculty_id=validated_data['faculty_id'],
                department=validated_data['department'],
                title=validated_data['title'],
                office_location=validated_data.get('office_location', ''),
                research_area=validated_data.get('research_area', '')
            )
        
        elif role_code == 'administrator':
            Administrator.objects.create(
                user=user,
                admin_id=validated_data['admin_id'],
                department=validated_data['department'],
                position=validated_data['position']
            )
        
        return user


class LoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField(help_text='用户名')
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        """验证用户名和密码"""
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise serializers.ValidationError('该账号已被禁用')
            data['user'] = user
        else:
            raise serializers.ValidationError('必须提供用户名和密码')
        
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_old_password(self, value):
        """验证旧密码是否正确"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('旧密码不正确')
        return value
    
    def validate(self, data):
        """验证新密码是否一致"""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({'new_password': '两次输入的新密码不一致'})
        
        # 使用Django的密码验证器
        try:
            validate_password(data['new_password'], self.context['request'].user)
        except Exception as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        
        return data
    
    def save(self):
        """保存新密码"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# ==============================================================================
# JWT Token 自定义序列化器
# ==============================================================================

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义JWT Token序列化器
    在token中添加用户角色和权限信息
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # 添加自定义声明
        token['username'] = user.username
        token['real_name'] = user.real_name
        token['email'] = user.email
        
        # 添加角色信息
        primary_role = user.get_primary_role()
        if primary_role:
            token['role_code'] = primary_role.role_code
            token['role_name'] = primary_role.role_name
        
        # 添加权限列表
        permissions = user.get_all_permissions_list()
        token['permissions'] = [p.permission_code for p in permissions]
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # 添加用户完整信息到响应中
        data['user'] = UserSerializer(self.user).data
        
        return data
