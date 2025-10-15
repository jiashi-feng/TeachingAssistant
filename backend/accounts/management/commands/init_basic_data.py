"""
初始化基础数据：角色、权限、角色权限关联
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import Role, Permission, RolePermission


class Command(BaseCommand):
    help = '初始化系统基础数据：角色、权限、角色权限关联'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始初始化基础数据...'))
        
        with transaction.atomic():
            # 1. 创建角色
            self.create_roles()
            
            # 2. 创建权限
            self.create_permissions()
            
            # 3. 分配权限给角色
            self.assign_permissions_to_roles()
        
        self.stdout.write(self.style.SUCCESS('✅ 基础数据初始化完成！'))
    
    def create_roles(self):
        """创建基础角色"""
        self.stdout.write('创建角色...')
        
        roles_data = [
            {
                'role_code': 'student',
                'role_name': '学生',
                'description': '普通学生用户，可以浏览和申请岗位'
            },
            {
                'role_code': 'faculty',
                'role_name': '教师',
                'description': '教师用户，可以发布岗位、审核申请和工时'
            },
            {
                'role_code': 'admin',
                'role_name': '管理员',
                'description': '系统管理员，拥有最高权限'
            },
        ]
        
        for data in roles_data:
            role, created = Role.objects.get_or_create(
                role_code=data['role_code'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ 创建角色: {role.role_name}')
            else:
                self.stdout.write(f'  - 角色已存在: {role.role_name}')
    
    def create_permissions(self):
        """创建所有权限"""
        self.stdout.write('创建权限...')
        
        permissions_data = [
            # ========== 用户管理权限 ==========
            {
                'permission_code': 'manage_user',
                'permission_name': '管理用户',
                'module': 'accounts',
                'description': '增删改查用户'
            },
            {
                'permission_code': 'manage_role',
                'permission_name': '管理角色',
                'module': 'accounts',
                'description': '分配和撤销角色'
            },
            
            # ========== 岗位管理权限 ==========
            {
                'permission_code': 'view_position',
                'permission_name': '浏览岗位',
                'module': 'recruitment',
                'description': '查看开放岗位列表'
            },
            {
                'permission_code': 'create_position',
                'permission_name': '创建岗位',
                'module': 'recruitment',
                'description': '发布新的助教岗位'
            },
            {
                'permission_code': 'manage_own_position',
                'permission_name': '管理自己的岗位',
                'module': 'recruitment',
                'description': '编辑或关闭自己发布的岗位'
            },
            {
                'permission_code': 'manage_all_position',
                'permission_name': '管理所有岗位',
                'module': 'recruitment',
                'description': '管理所有岗位（管理员权限）'
            },
            
            # ========== 申请管理权限 ==========
            {
                'permission_code': 'apply_position',
                'permission_name': '申请岗位',
                'module': 'application',
                'description': '提交岗位申请'
            },
            {
                'permission_code': 'view_own_application',
                'permission_name': '查看自己的申请',
                'module': 'application',
                'description': '查看申请状态'
            },
            {
                'permission_code': 'review_application',
                'permission_name': '审核申请',
                'module': 'application',
                'description': '审核学生的岗位申请'
            },
            
            # ========== 工时管理权限 ==========
            {
                'permission_code': 'submit_timesheet',
                'permission_name': '提交工时',
                'module': 'timesheet',
                'description': '提交工时表'
            },
            {
                'permission_code': 'view_own_timesheet',
                'permission_name': '查看自己的工时',
                'module': 'timesheet',
                'description': '查看工时记录'
            },
            {
                'permission_code': 'review_timesheet',
                'permission_name': '审核工时',
                'module': 'timesheet',
                'description': '审核助教的工时表'
            },
            
            # ========== 薪酬管理权限 ==========
            {
                'permission_code': 'view_own_salary',
                'permission_name': '查看自己的薪酬',
                'module': 'timesheet',
                'description': '查看薪酬记录'
            },
            {
                'permission_code': 'generate_salary_report',
                'permission_name': '生成薪酬报表',
                'module': 'timesheet',
                'description': '管理员生成月度薪酬报表'
            },
            {
                'permission_code': 'manage_payment',
                'permission_name': '管理支付',
                'module': 'timesheet',
                'description': '标记薪酬支付状态'
            },
            
            # ========== 数据统计权限 ==========
            {
                'permission_code': 'view_own_dashboard',
                'permission_name': '查看个人看板',
                'module': 'dashboard',
                'description': '查看个人数据统计'
            },
            {
                'permission_code': 'view_all_dashboard',
                'permission_name': '查看全局看板',
                'module': 'dashboard',
                'description': '查看全平台数据统计'
            },
            {
                'permission_code': 'export_report',
                'permission_name': '导出报表',
                'module': 'dashboard',
                'description': '导出Excel报表'
            },
        ]
        
        for data in permissions_data:
            perm, created = Permission.objects.get_or_create(
                permission_code=data['permission_code'],
                defaults=data
            )
            if created:
                self.stdout.write(f'  ✓ 创建权限: {perm.permission_name}')
            else:
                self.stdout.write(f'  - 权限已存在: {perm.permission_name}')
    
    def assign_permissions_to_roles(self):
        """为角色分配权限"""
        self.stdout.write('分配权限给角色...')
        
        # 获取角色
        student_role = Role.objects.get(role_code='student')
        faculty_role = Role.objects.get(role_code='faculty')
        admin_role = Role.objects.get(role_code='admin')
        
        # ========== 学生角色的权限 ==========
        student_permissions = [
            'view_position',           # 浏览岗位
            'apply_position',          # 申请岗位
            'view_own_application',    # 查看自己的申请
            'submit_timesheet',        # 提交工时（成为助教后）
            'view_own_timesheet',      # 查看自己的工时
            'view_own_salary',         # 查看自己的薪酬
            'view_own_dashboard',      # 查看个人看板
        ]
        
        self.stdout.write(f'  为 {student_role.role_name} 分配权限...')
        for perm_code in student_permissions:
            perm = Permission.objects.get(permission_code=perm_code)
            _, created = RolePermission.objects.get_or_create(
                role=student_role,
                permission=perm
            )
            if created:
                self.stdout.write(f'    ✓ {perm.permission_name}')
        
        # ========== 教师角色的权限 ==========
        faculty_permissions = [
            'view_position',           # 浏览岗位
            'create_position',         # 创建岗位
            'manage_own_position',     # 管理自己的岗位
            'review_application',      # 审核申请
            'review_timesheet',        # 审核工时
            'view_own_dashboard',      # 查看个人看板
        ]
        
        self.stdout.write(f'  为 {faculty_role.role_name} 分配权限...')
        for perm_code in faculty_permissions:
            perm = Permission.objects.get(permission_code=perm_code)
            _, created = RolePermission.objects.get_or_create(
                role=faculty_role,
                permission=perm
            )
            if created:
                self.stdout.write(f'    ✓ {perm.permission_name}')
        
        # ========== 管理员角色的权限（所有权限） ==========
        all_permissions = Permission.objects.all()
        
        self.stdout.write(f'  为 {admin_role.role_name} 分配所有权限...')
        count = 0
        for perm in all_permissions:
            _, created = RolePermission.objects.get_or_create(
                role=admin_role,
                permission=perm
            )
            if created:
                count += 1
        self.stdout.write(f'    ✓ 分配了 {count} 个权限')

