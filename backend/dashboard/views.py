"""
学生助教管理平台 - 数据看板模块视图
包含：管理员月度报表API、导出、趋势
"""

import csv
from io import StringIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum, Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from accounts.permissions import IsAdministrator
from accounts.models import User
from recruitment.models import Position
from application.models import Application
from timesheet.models import Timesheet, Salary


def get_monthly_stats(year, month):
    """公共：按年月计算统计，返回 period + statistics 字典。"""
    start_date = datetime(year, month, 1).date()
    if month == 12:
        end_date = datetime(year + 1, 1, 1).date() - timedelta(days=1)
    else:
        end_date = datetime(year + 1, month + 1, 1).date() - timedelta(days=1)
    total_users = User.objects.count()
    students = User.objects.filter(userrole__role__role_code='student').distinct().count()
    faculty = User.objects.filter(userrole__role__role_code='faculty').distinct().count()
    administrators = User.objects.filter(userrole__role__role_code='administrator').distinct().count()
    positions_created = Position.objects.filter(created_at__year=year, created_at__month=month).count()
    total_positions = Position.objects.count()
    open_positions = Position.objects.filter(status='open').count()
    applications_submitted = Application.objects.filter(applied_at__year=year, applied_at__month=month).count()
    total_applications = Application.objects.count()
    pending_applications = Application.objects.filter(status__in=['submitted', 'reviewing']).count()
    accepted_applications = Application.objects.filter(status='accepted').count()
    timesheets_submitted = Timesheet.objects.filter(submitted_at__year=year, submitted_at__month=month).count()
    total_timesheets = Timesheet.objects.count()
    pending_timesheets = Timesheet.objects.filter(status='pending').count()
    approved_timesheets = Timesheet.objects.filter(status='approved').count()
    salaries_generated = Salary.objects.filter(generated_at__year=year, generated_at__month=month)
    monthly_salary_total = salaries_generated.aggregate(total=Sum('amount'))['total'] or 0
    monthly_salary_count = salaries_generated.count()
    paid_salary_count = salaries_generated.filter(payment_status='paid').count()
    total_salary = Salary.objects.aggregate(total=Sum('amount'))['total'] or 0
    return {
        'period': {'year': year, 'month': month, 'start_date': start_date.isoformat(), 'end_date': end_date.isoformat()},
        'statistics': {
            'total_users': total_users, 'students': students, 'faculty': faculty, 'administrators': administrators,
            'positions_created_this_month': positions_created, 'total_positions': total_positions, 'open_positions': open_positions,
            'applications_submitted_this_month': applications_submitted, 'total_applications': total_applications,
            'pending_applications': pending_applications, 'accepted_applications': accepted_applications,
            'timesheets_submitted_this_month': timesheets_submitted, 'total_timesheets': total_timesheets,
            'pending_timesheets': pending_timesheets, 'approved_timesheets': approved_timesheets,
            'salaries_generated_this_month': monthly_salary_count, 'monthly_salary_total': float(monthly_salary_total),
            'paid_salary_count_this_month': paid_salary_count, 'total_salary': float(total_salary),
        },
    }


def get_trends_data(metric, group_by, start_year, end_year):
    """
    公共：按指标与时间维度聚合趋势数据
    metric: positions|applications|timesheets|salaries
    group_by: month|year
    """
    result = []
    if metric == 'positions':
        qs = Position.objects.filter(created_at__year__gte=start_year, created_at__year__lte=end_year)
        if group_by == 'year':
            qs = qs.annotate(yr=ExtractYear('created_at')).values('yr').annotate(count=Count('position_id')).order_by('yr')
            result = [{'year': r['yr'], 'count': r['count']} for r in qs]
        else:
            qs = qs.annotate(yr=ExtractYear('created_at'), mo=ExtractMonth('created_at')).values('yr', 'mo').annotate(count=Count('position_id')).order_by('yr', 'mo')
            result = [{'year': r['yr'], 'month': r['mo'], 'count': r['count']} for r in qs]
    elif metric == 'applications':
        qs = Application.objects.filter(applied_at__year__gte=start_year, applied_at__year__lte=end_year)
        if group_by == 'year':
            qs = qs.annotate(yr=ExtractYear('applied_at')).values('yr').annotate(count=Count('application_id')).order_by('yr')
            result = [{'year': r['yr'], 'count': r['count']} for r in qs]
        else:
            qs = qs.annotate(yr=ExtractYear('applied_at'), mo=ExtractMonth('applied_at')).values('yr', 'mo').annotate(count=Count('application_id')).order_by('yr', 'mo')
            result = [{'year': r['yr'], 'month': r['mo'], 'count': r['count']} for r in qs]
    elif metric == 'timesheets':
        qs = Timesheet.objects.filter(month__year__gte=start_year, month__year__lte=end_year)
        if group_by == 'year':
            qs = qs.values('month__year').annotate(count=Count('timesheet_id')).order_by('month__year')
            result = [{'year': r['month__year'], 'count': r['count']} for r in qs]
        else:
            qs = qs.values('month__year', 'month__month').annotate(count=Count('timesheet_id')).order_by('month__year', 'month__month')
            result = [{'year': r['month__year'], 'month': r['month__month'], 'count': r['count']} for r in qs]
    elif metric == 'salaries':
        qs = Salary.objects.filter(generated_at__year__gte=start_year, generated_at__year__lte=end_year)
        if group_by == 'year':
            qs = qs.annotate(yr=ExtractYear('generated_at')).values('yr').annotate(count=Count('salary_id'), total=Sum('amount')).order_by('yr')
            result = [{'year': r['yr'], 'count': r['count'], 'total': float(r['total'] or 0)} for r in qs]
        else:
            qs = qs.annotate(yr=ExtractYear('generated_at'), mo=ExtractMonth('generated_at')).values('yr', 'mo').annotate(count=Count('salary_id'), total=Sum('amount')).order_by('yr', 'mo')
            result = [{'year': r['yr'], 'month': r['mo'], 'count': r['count'], 'total': float(r['total'] or 0)} for r in qs]
    else:
        raise ValueError('metric_invalid')
    return result


class MonthlyReport(APIView):
    """GET /api/admin/reports/monthly/?year=&month="""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def get(self, request):
        now = timezone.now()
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        year = int(year) if year else now.year
        month = int(month) if month else now.month
        return Response(get_monthly_stats(year, month))


class MonthlyReportExport(APIView):
    """GET /api/admin/reports/export/?year=&month=&format=csv"""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def get(self, request):
        now = timezone.now()
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        fmt = (request.query_params.get('format') or 'csv').lower()
        year = int(year) if year else now.year
        month = int(month) if month else now.month
        data = get_monthly_stats(year, month)
        stats = data['statistics']
        buf = StringIO()
        w = csv.writer(buf)
        w.writerow(['月度报表', f'{year}年{month}月'])
        w.writerow([])
        w.writerow(['指标', '数值'])
        w.writerow(['用户总数', stats['total_users']])
        w.writerow(['学生数', stats['students']])
        w.writerow(['教师数', stats['faculty']])
        w.writerow(['管理员数', stats['administrators']])
        w.writerow(['本月新岗位数', stats['positions_created_this_month']])
        w.writerow(['岗位总数', stats['total_positions']])
        w.writerow(['开放岗位数', stats['open_positions']])
        w.writerow(['本月新申请数', stats['applications_submitted_this_month']])
        w.writerow(['申请总数', stats['total_applications']])
        w.writerow(['待审核申请', stats['pending_applications']])
        w.writerow(['已录用申请', stats['accepted_applications']])
        w.writerow(['本月提交工时数', stats['timesheets_submitted_this_month']])
        w.writerow(['工时表总数', stats['total_timesheets']])
        w.writerow(['待审核工时', stats['pending_timesheets']])
        w.writerow(['已批准工时', stats['approved_timesheets']])
        w.writerow(['本月生成薪酬条数', stats['salaries_generated_this_month']])
        w.writerow(['本月薪酬总额', stats['monthly_salary_total']])
        w.writerow(['本月已支付条数', stats['paid_salary_count_this_month']])
        w.writerow(['薪酬总累计', stats['total_salary']])
        resp = HttpResponse(buf.getvalue(), content_type='text/csv; charset=utf-8-sig')
        resp['Content-Disposition'] = f'attachment; filename="monthly_report_{year}_{month:02d}.csv"'
        return resp


class TrendsReport(APIView):
    """GET /api/admin/reports/trends/?metric=positions|applications|timesheets|salaries&group_by=month|year&start_year=&end_year="""
    permission_classes = [permissions.IsAuthenticated, IsAdministrator]

    def get(self, request):
        metric = request.query_params.get('metric', 'positions')
        group_by = request.query_params.get('group_by', 'month')
        start_year = request.query_params.get('start_year')
        end_year = request.query_params.get('end_year')
        now = timezone.now()
        start_year = int(start_year) if start_year else now.year - 2
        end_year = int(end_year) if end_year else now.year
        try:
            result = get_trends_data(metric, group_by, start_year, end_year)
        except ValueError:
            return Response({'detail': 'metric 可选: positions, applications, timesheets, salaries'}, status=400)
        return Response({'metric': metric, 'group_by': group_by, 'start_year': start_year, 'end_year': end_year, 'data': result})
