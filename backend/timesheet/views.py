"""
学生助教管理平台 - 工时管理模块视图
包含：助教端工时管理、薪酬查询、助教看板
"""

from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Q
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from accounts.permissions import IsTA, IsFaculty
from .models import Timesheet, Salary
from .serializers import (
    TimesheetCreateSerializer,
    TimesheetUpdateSerializer,
    TimesheetListSerializer,
    TimesheetDetailSerializer,
    TimesheetReviewSerializer,
    SalaryListSerializer,
    SalaryDetailSerializer,
)
from application.models import Application


class TimesheetListCreate(generics.ListCreateAPIView):
    """
    工时表列表和创建
    GET /api/ta/timesheets/ - 我的工时列表
    POST /api/ta/timesheets/ - 提交工时表
    支持筛选：status, position, month
    支持排序：-month, -submitted_at
    """
    permission_classes = [permissions.IsAuthenticated, IsTA]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'position', 'month']
    ordering_fields = ['month', 'submitted_at']
    ordering = ['-month', '-submitted_at']
    
    def get_queryset(self):
        """获取当前助教的工时表列表"""
        return Timesheet.objects.filter(
            ta=self.request.user
        ).select_related(
            'position',
            'ta',
            'reviewed_by'
        )
    
    def get_serializer_class(self):
        """根据请求方法返回不同的序列化器"""
        if self.request.method == 'POST':
            return TimesheetCreateSerializer
        return TimesheetListSerializer
    
    def perform_create(self, serializer):
        """创建工时表"""
        # 修复：不需要传递 ta，因为序列化器的 create() 方法会从 context 中获取
        serializer.save()


class MyTimesheetDetail(generics.RetrieveAPIView):
    """
    我的工时详情
    GET /api/ta/timesheets/{timesheet_id}/
    """
    permission_classes = [permissions.IsAuthenticated, IsTA]
    serializer_class = TimesheetDetailSerializer
    lookup_field = 'timesheet_id'
    
    def get_queryset(self):
        """只允许查看自己的工时表"""
        return Timesheet.objects.filter(
            ta=self.request.user
        ).select_related(
            'position',
            'ta',
            'reviewed_by'
        )


class UpdateTimesheet(generics.UpdateAPIView):
    """
    编辑工时表（仅限待审核状态）
    PUT /api/ta/timesheets/{timesheet_id}/
    """
    permission_classes = [permissions.IsAuthenticated, IsTA]
    serializer_class = TimesheetUpdateSerializer
    lookup_field = 'timesheet_id'
    
    def get_queryset(self):
        """只允许编辑自己的待审核工时表"""
        return Timesheet.objects.filter(
            ta=self.request.user,
            status='pending'
        )


class MySalaries(generics.ListAPIView):
    """
    我的薪酬列表
    GET /api/ta/salaries/
    支持排序：-generated_at
    """
    permission_classes = [permissions.IsAuthenticated, IsTA]
    serializer_class = SalaryListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['generated_at']
    ordering = ['-generated_at']
    
    def get_queryset(self):
        """获取当前助教的薪酬记录列表"""
        return Salary.objects.filter(
            timesheet__ta=self.request.user
        ).select_related(
            'timesheet__position',
            'timesheet__ta',
            'generated_by'
        )


class SalaryDetail(generics.RetrieveAPIView):
    """
    薪酬详情
    GET /api/ta/salaries/{salary_id}/
    """
    permission_classes = [permissions.IsAuthenticated, IsTA]
    serializer_class = SalaryDetailSerializer
    lookup_field = 'salary_id'
    
    def get_queryset(self):
        """只允许查看自己的薪酬记录"""
        return Salary.objects.filter(
            timesheet__ta=self.request.user
        ).select_related(
            'timesheet__position',
            'timesheet__ta',
            'generated_by'
        )


class TADashboard(APIView):
    """
    助教看板数据统计
    GET /api/ta/dashboard/
    """
    permission_classes = [permissions.IsAuthenticated, IsTA]
    
    def get(self, request):
        """获取助教看板统计数据"""
        user = request.user
        
        # 统计工时表数据
        timesheets = Timesheet.objects.filter(ta=user)
        total_timesheets = timesheets.count()
        pending_timesheets = timesheets.filter(status='pending').count()
        approved_timesheets = timesheets.filter(status='approved').count()
        rejected_timesheets = timesheets.filter(status='rejected').count()
        
        # 统计薪酬数据
        salaries = Salary.objects.filter(timesheet__ta=user)
        total_salary = salaries.aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        paid_salary = salaries.filter(payment_status='paid').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        pending_salary = salaries.filter(payment_status='pending').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # 统计在岗岗位数（有已通过的申请）
        active_positions = Application.objects.filter(
            applicant=user,
            status='accepted'
        ).count()
        
        # 获取最近的工时表（最近3条）
        recent_timesheets = timesheets.select_related(
            'position'
        )[:3]
        recent_timesheets_data = TimesheetListSerializer(
            recent_timesheets,
            many=True
        ).data
        
        # 获取最近的薪酬记录（最近3条）
        recent_salaries = salaries.select_related(
            'timesheet__position'
        )[:3]
        recent_salaries_data = SalaryListSerializer(
            recent_salaries,
            many=True
        ).data
        
        return Response({
            'statistics': {
                'total_timesheets': total_timesheets,
                'pending_timesheets': pending_timesheets,
                'approved_timesheets': approved_timesheets,
                'rejected_timesheets': rejected_timesheets,
                'active_positions': active_positions,
                'total_salary': float(total_salary),
                'paid_salary': float(paid_salary),
                'pending_salary': float(pending_salary),
            },
            'recent_timesheets': recent_timesheets_data,
            'recent_salaries': recent_salaries_data,
        })


class FacultyTimesheetList(generics.ListAPIView):
    """
    教师端：我的岗位工时列表
    GET /api/faculty/timesheets/
    支持筛选：status, position, month
    支持排序：-month, -submitted_at
    """
    permission_classes = [permissions.IsAuthenticated, IsFaculty]
    serializer_class = TimesheetListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'position', 'month']
    ordering_fields = ['month', 'submitted_at']
    ordering = ['-month', '-submitted_at']
    
    def get_queryset(self):
        """获取当前教师发布的岗位的所有工时表"""
        return Timesheet.objects.filter(
            position__posted_by=self.request.user
        ).select_related(
            'position',
            'ta',
            'reviewed_by'
        )


class FacultyTimesheetDetail(generics.RetrieveAPIView):
    """
    教师端：工时详情
    GET /api/faculty/timesheets/{timesheet_id}/
    """
    permission_classes = [permissions.IsAuthenticated, IsFaculty]
    serializer_class = TimesheetDetailSerializer
    lookup_field = 'timesheet_id'

    def get_queryset(self):
        """只允许查看自己岗位下的工时表"""
        return Timesheet.objects.filter(
            position__posted_by=self.request.user
        ).select_related(
            'position',
            'ta',
            'reviewed_by'
        )


class ReviewTimesheet(APIView):
    """
    教师端：审核工时表
    POST /api/faculty/timesheets/{timesheet_id}/review/
    """
    permission_classes = [permissions.IsAuthenticated, IsFaculty]
    
    def post(self, request, timesheet_id):
        """审核工时表"""
        timesheet = get_object_or_404(
            Timesheet.objects.select_related('position', 'ta'),
            timesheet_id=timesheet_id
        )
        
        # 验证：必须是该岗位的发布教师
        if timesheet.position.posted_by != request.user:
            return Response(
                {'detail': '无权审核该工时表'},
                status=403
            )
        
        # 验证：只能审核待审核状态的工时表
        if timesheet.status != 'pending':
            return Response(
                {'detail': '只能审核待审核状态的工时表'},
                status=400
            )
        
        # 验证请求数据
        serializer = TimesheetReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data['action']
        review_notes = serializer.validated_data.get('review_notes', '')
        
        # 更新工时表状态
        with transaction.atomic():
            timesheet.status = 'approved' if action == 'approve' else 'rejected'
            timesheet.reviewed_by = request.user
            timesheet.reviewed_at = timezone.now()
            timesheet.review_notes = review_notes
            timesheet.save(update_fields=['status', 'reviewed_by', 'reviewed_at', 'review_notes', 'updated_at'])
        
        return Response({
            'status': timesheet.status,
            'status_display': timesheet.get_status_display(),
            'reviewed_at': timesheet.reviewed_at,
        })
