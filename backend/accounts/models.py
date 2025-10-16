"""
学生助教管理平台 - 用户认证模块模型
包含：User, Role, Permission, UserRole, RolePermission, Student, Faculty, Administrator
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.utils import timezone


# ==============================================================================
# 自定义用户管理器
# ==============================================================================

class UserManager(BaseUserManager):
    """自定义用户管理器"""
    
    def create_user(self, username, email, password=None, user_id=None, **extra_fields):
        """
        创建普通用户
        
        Args:
            username: 用户名（登录用）
            email: 邮箱
            password: 密码
            user_id: 用户ID（主键），如 S2021001234
            **extra_fields: 其他字段（如 real_name, phone等）
        """
        if not username:
            raise ValueError('用户名不能为空')
        if not email:
            raise ValueError('邮箱不能为空')
        if not user_id:
            raise ValueError('用户ID不能为空')
        
        email = self.normalize_email(email)
        
        # 创建用户时必须传入user_id（主键）
        user = self.model(
            user_id=user_id,  # 主键必须在创建时就指定
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, user_id=None, **extra_fields):
        """
        创建超级用户
        
        注意：命令行创建超级用户时，user_id需要手动输入
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置 is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 is_superuser=True')
        
        # 如果没有提供user_id，生成一个默认的管理员ID
        if not user_id:
            # 查找最大的管理员ID
            import re
            admin_users = self.filter(user_id__startswith='A').order_by('-user_id')
            if admin_users.exists():
                last_id = admin_users.first().user_id
                # 提取数字部分并+1
                match = re.search(r'A(\d+)', last_id)
                if match:
                    next_num = int(match.group(1)) + 1
                    user_id = f'A{next_num:05d}'  # A00001, A00002...
                else:
                    user_id = 'A00001'
            else:
                user_id = 'A00001'
        
        return self.create_user(username, email, password, user_id=user_id, **extra_fields)


# ==============================================================================
# 核心用户表
# ==============================================================================

class User(AbstractBaseUser, PermissionsMixin):
    """
    核心用户表 - 所有用户的基础信息
    user_id格式: S+学号(学生) / F+工号(教师) / A+编号(管理员)
    """
    
    user_id = models.CharField(
        max_length=20,
        primary_key=True,
        verbose_name='用户ID',
        help_text='格式: S2021001234(学生) / F20210001(教师) / A00001(管理员)'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='用户名',
        validators=[MinLengthValidator(3, '用户名至少3个字符')]
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='邮箱'
    )
    real_name = models.CharField(
        max_length=50,
        verbose_name='真实姓名'
    )
    phone = models.CharField(
        max_length=11,
        null=True,
        blank=True,
        verbose_name='手机号'
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
        null=True,
        blank=True,
        verbose_name='头像'
    )
    
    # Django required fields
    is_active = models.BooleanField(
        default=True,
        verbose_name='账号是否激活'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='是否为员工'
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='注册时间'
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='最后登录时间'
    )
    
    # 时间戳
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'real_name']
    
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f'{self.username} ({self.real_name})'
    
    def get_primary_role(self):
        """获取用户的主角色"""
        try:
            user_role = self.userrole_set.filter(is_primary=True).first()
            return user_role.role if user_role else None
        except Exception:
            return None
    
    def has_permission(self, permission_code):
        """检查用户是否拥有某个权限"""
        return Permission.objects.filter(
            rolepermission__role__userrole__user=self,
            permission_code=permission_code
        ).exists()
    
    def get_all_permissions_list(self):
        """获取用户的所有权限列表"""
        return Permission.objects.filter(
            rolepermission__role__userrole__user=self
        ).distinct()


# ==============================================================================
# 角色表
# ==============================================================================

class Role(models.Model):
    """角色表 - 定义系统中的所有角色"""
    
    role_id = models.AutoField(
        primary_key=True,
        verbose_name='角色ID'
    )
    role_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='角色代码',
        help_text='如: student, faculty, admin'
    )
    role_name = models.CharField(
        max_length=50,
        verbose_name='角色名称'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='角色描述'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        db_table = 'role'
        verbose_name = '角色'
        verbose_name_plural = '角色'
        ordering = ['role_id']
    
    def __str__(self):
        return self.role_name


# ==============================================================================
# 权限表
# ==============================================================================

class Permission(models.Model):
    """权限表 - 定义系统中的所有权限"""
    
    permission_id = models.AutoField(
        primary_key=True,
        verbose_name='权限ID'
    )
    permission_code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='权限代码',
        help_text='如: view_position, create_position'
    )
    permission_name = models.CharField(
        max_length=100,
        verbose_name='权限名称'
    )
    module = models.CharField(
        max_length=50,
        verbose_name='所属模块',
        help_text='如: recruitment, application, timesheet'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='权限描述'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        db_table = 'permission'
        verbose_name = '权限'
        verbose_name_plural = '权限'
        ordering = ['module', 'permission_code']
        indexes = [
            models.Index(fields=['module']),
        ]
    
    def __str__(self):
        return f'{self.permission_name} ({self.permission_code})'


# ==============================================================================
# 用户角色关联表
# ==============================================================================

class UserRole(models.Model):
    """用户角色关联表 - 支持一个用户拥有多个角色"""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name='角色'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='是否为主角色'
    )
    assigned_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='分配时间'
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_roles',
        verbose_name='分配人'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        db_table = 'user_role'
        verbose_name = '用户角色'
        verbose_name_plural = '用户角色'
        unique_together = [['user', 'role']]
        ordering = ['-is_primary', '-assigned_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        primary_tag = '[主]' if self.is_primary else ''
        return f'{self.user.username} - {self.role.role_name} {primary_tag}'


# ==============================================================================
# 角色权限关联表
# ==============================================================================

class RolePermission(models.Model):
    """角色权限关联表 - 定义每个角色拥有的权限"""
    
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name='角色'
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        verbose_name='权限'
    )
    granted_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='授权时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        db_table = 'role_permission'
        verbose_name = '角色权限'
        verbose_name_plural = '角色权限'
        unique_together = [['role', 'permission']]
        ordering = ['role', 'permission']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['permission']),
        ]
    
    def __str__(self):
        return f'{self.role.role_name} - {self.permission.permission_name}'


# ==============================================================================
# 学生信息表
# ==============================================================================

class Student(models.Model):
    """学生信息表 - 存储学生特有的信息"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='关联用户'
    )
    student_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='学号'
    )
    department = models.CharField(
        max_length=100,
        verbose_name='院系'
    )
    major = models.CharField(
        max_length=100,
        verbose_name='专业'
    )
    grade = models.IntegerField(
        verbose_name='年级',
        help_text='如: 2021'
    )
    class_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='班级'
    )
    is_ta = models.BooleanField(
        default=False,
        verbose_name='是否为助教'
    )
    ta_since = models.DateField(
        null=True,
        blank=True,
        verbose_name='成为助教时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'student'
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'
        ordering = ['-grade', 'student_id']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['department']),
            models.Index(fields=['is_ta']),
        ]
    
    def __str__(self):
        return f'{self.student_id} - {self.user.real_name}'


# ==============================================================================
# 教师信息表
# ==============================================================================

class Faculty(models.Model):
    """教师信息表 - 存储教师特有的信息"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='关联用户'
    )
    faculty_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='工号'
    )
    department = models.CharField(
        max_length=100,
        verbose_name='院系'
    )
    title = models.CharField(
        max_length=50,
        verbose_name='职称',
        help_text='如: 教授, 副教授, 讲师'
    )
    office_location = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='办公室'
    )
    research_area = models.TextField(
        null=True,
        blank=True,
        verbose_name='研究方向'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'faculty'
        verbose_name = '教师信息'
        verbose_name_plural = '教师信息'
        ordering = ['faculty_id']
        indexes = [
            models.Index(fields=['faculty_id']),
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return f'{self.faculty_id} - {self.user.real_name} ({self.title})'


# ==============================================================================
# 管理员信息表
# ==============================================================================

class Administrator(models.Model):
    """管理员信息表 - 存储管理员特有的信息"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='关联用户'
    )
    admin_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='管理员编号'
    )
    department = models.CharField(
        max_length=100,
        verbose_name='部门'
    )
    position = models.CharField(
        max_length=50,
        verbose_name='职位'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'administrator'
        verbose_name = '管理员信息'
        verbose_name_plural = '管理员信息'
        ordering = ['admin_id']
        indexes = [
            models.Index(fields=['admin_id']),
            models.Index(fields=['department']),
        ]
    
    def __str__(self):
        return f'{self.admin_id} - {self.user.real_name} ({self.position})'
