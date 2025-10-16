"""
Context Processors
为Admin模板添加全局上下文数据
"""

from django.db.models import Sum, Count
from datetime import datetime

from accounts.models import User
from recruitment.models import Position
from application.models import Application
from timesheet.models import Timesheet, Salary


def admin_stats(request):
    """
    Admin统计数据context processor
    仅在admin页面生效
    """
    # 只在admin页面添加统计数据
    if not request.path.startswith('/admin'):
        return {}
    
    try:
        # 用户统计
        user_count = User.objects.count()
        
        # 岗位统计
        position_count = Position.objects.count()
        
        # 申请统计
        application_count = Application.objects.count()
        pending_applications = Application.objects.filter(status='pending').count()
        
        # 本月薪酬
        current_month = datetime.now().month
        current_year = datetime.now().year
        monthly_salary = Salary.objects.filter(
            month__month=current_month,
            month__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return {
            'user_count': user_count,
            'position_count': position_count,
            'application_count': application_count,
            'pending_applications': pending_applications,
            'monthly_salary': f"{monthly_salary:,.0f}",
        }
    except Exception as e:
        print(f"统计数据获取失败: {e}")
        return {
            'user_count': 0,
            'position_count': 0,
            'application_count': 0,
            'pending_applications': 0,
            'monthly_salary': '0',
        }

