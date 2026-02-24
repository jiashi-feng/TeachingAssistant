"""
自定义Admin视图
提供管理员仪表板的统计数据
"""

from django.contrib import admin
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime

from accounts.models import User
from recruitment.models import Position
from application.models import Application
from timesheet.models import Timesheet, Salary


class CustomAdminSite(admin.AdminSite):
    """
    自定义Admin站点
    重写index方法以添加统计数据
    """
    
    site_header = "学生助教管理系统"
    site_title = "助教管理平台"
    index_title = "管理后台"
    
    def index(self, request, extra_context=None):
        """
        重写index方法，添加统计数据到context
        """
        extra_context = extra_context or {}
        
        try:
            # 用户统计
            extra_context['user_count'] = User.objects.count()
            extra_context['student_count'] = User.objects.filter(
                userrole__role__role_code='student'
            ).distinct().count()
            extra_context['faculty_count'] = User.objects.filter(
                userrole__role__role_code='faculty'
            ).distinct().count()
            
            # 岗位统计
            extra_context['position_count'] = Position.objects.count()
            extra_context['open_positions'] = Position.objects.filter(status='open').count()
            
            # 申请统计
            extra_context['application_count'] = Application.objects.count()
            # 修复：待审核= submitted/reviewing 两种状态
            extra_context['pending_applications'] = Application.objects.filter(
                status__in=['submitted', 'reviewing']
            ).count()
            extra_context['accepted_applications'] = Application.objects.filter(
                status='accepted'
            ).count()
            
            # 工时统计
            extra_context['pending_timesheets'] = Timesheet.objects.filter(
                status='pending'
            ).count()
            
            # 本月薪酬统计
            now = datetime.now()
            monthly_salary = Salary.objects.filter(
                timesheet__month__year=now.year,
                timesheet__month__month=now.month,
            ).aggregate(total=Sum('amount'))['total'] or 0
            extra_context['monthly_salary'] = f"{monthly_salary:,.0f}"
            
        except Exception as e:
            print(f"统计数据获取失败: {e}")
            # 设置默认值
            extra_context.update({
                'user_count': 0,
                'student_count': 0,
                'faculty_count': 0,
                'position_count': 0,
                'open_positions': 0,
                'application_count': 0,
                'pending_applications': 0,
                'accepted_applications': 0,
                'pending_timesheets': 0,
                'monthly_salary': '0',
            })
        
        return super().index(request, extra_context)


# 创建自定义admin站点实例
custom_admin_site = CustomAdminSite(name='custom_admin')

