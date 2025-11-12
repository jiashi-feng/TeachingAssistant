"""
学生助教管理平台 - 数据看板模块视图
包含：管理员月度报表API
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.permissions import IsAdministrator
from accounts.models import User
from recruitment.models import Position
from application.models import Application
from timesheet.models import Timesheet, Salary


class MonthlyReport(APIView):
    """
    管理员月度报表
    GET /api/admin/reports/monthly/
    支持查询参数：year, month（默认当前月份）
    """
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]
    
    def get(self, request):
        """获取月度报表数据"""
        # 获取查询参数
        year = request.query_params.get('year', None)
        month = request.query_params.get('month', None)
        
        # 如果没有指定，使用当前月份
        now = timezone.now()
        if not year:
            year = now.year
        else:
            year = int(year)
        if not month:
            month = now.month
        else:
            month = int(month)
        
        # 计算月份的开始和结束日期
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1).date() - timedelta(days=1)
        
        # 用户统计
        total_users = User.objects.count()
        students = User.objects.filter(
            roles__role__role_code='student'
        ).distinct().count()
        faculty = User.objects.filter(
            roles__role__role_code='faculty'
        ).distinct().count()
        administrators = User.objects.filter(
            roles__role__role_code='administrator'
        ).distinct().count()
        
        # 岗位统计（该月创建的岗位）
        positions_created = Position.objects.filter(
            created_at__year=year,
            created_at__month=month
        ).count()
        total_positions = Position.objects.count()
        open_positions = Position.objects.filter(status='open').count()
        
        # 申请统计（该月提交的申请）
        applications_submitted = Application.objects.filter(
            applied_at__year=year,
            applied_at__month=month
        ).count()
        total_applications = Application.objects.count()
        pending_applications = Application.objects.filter(
            status__in=['submitted', 'reviewing']
        ).count()
        accepted_applications = Application.objects.filter(status='accepted').count()
        
        # 工时统计（该月提交的工时）
        timesheets_submitted = Timesheet.objects.filter(
            submitted_at__year=year,
            submitted_at__month=month
        ).count()
        total_timesheets = Timesheet.objects.count()
        pending_timesheets = Timesheet.objects.filter(status='pending').count()
        approved_timesheets = Timesheet.objects.filter(status='approved').count()
        
        # 薪酬统计（该月生成的薪酬）
        salaries_generated = Salary.objects.filter(
            generated_at__year=year,
            generated_at__month=month
        )
        monthly_salary_total = salaries_generated.aggregate(
            total=Sum('amount')
        )['total'] or 0
        monthly_salary_count = salaries_generated.count()
        paid_salary_count = salaries_generated.filter(payment_status='paid').count()
        
        # 总薪酬统计
        total_salary = Salary.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        return Response({
            'period': {
                'year': year,
                'month': month,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
            },
            'statistics': {
                # 用户统计
                'total_users': total_users,
                'students': students,
                'faculty': faculty,
                'administrators': administrators,
                
                # 岗位统计
                'positions_created_this_month': positions_created,
                'total_positions': total_positions,
                'open_positions': open_positions,
                
                # 申请统计
                'applications_submitted_this_month': applications_submitted,
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'accepted_applications': accepted_applications,
                
                # 工时统计
                'timesheets_submitted_this_month': timesheets_submitted,
                'total_timesheets': total_timesheets,
                'pending_timesheets': pending_timesheets,
                'approved_timesheets': approved_timesheets,
                
                # 薪酬统计
                'salaries_generated_this_month': monthly_salary_count,
                'monthly_salary_total': float(monthly_salary_total),
                'paid_salary_count_this_month': paid_salary_count,
                'total_salary': float(total_salary),
            },
        })
