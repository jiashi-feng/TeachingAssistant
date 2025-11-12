from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from accounts.permissions import IsStudent, IsFaculty
from .models import Position
from .serializers import PositionListSerializer, PositionDetailSerializer, PositionCreateUpdateSerializer
from application.models import Application
from timesheet.models import Timesheet


class StudentPositionList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = PositionListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'course_code', 'posted_by']
    search_fields = ['title', 'course_name', 'description']
    ordering_fields = ['application_deadline', 'created_at']

    def get_queryset(self):
        from django.utils import timezone
        now = timezone.now()
        return Position.objects.filter(
            status='open',
            application_deadline__gte=now
        ).select_related('posted_by')


class StudentPositionDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = PositionDetailSerializer
    lookup_field = 'position_id'

    def get_queryset(self):
        return Position.objects.select_related('posted_by')


class FacultyPositionCreate(generics.CreateAPIView):
    pass


class FacultyPositionListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsFaculty]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'course_code']
    search_fields = ['title', 'course_name', 'description']
    ordering_fields = ['application_deadline', 'created_at']

    def get_queryset(self):
        return Position.objects.filter(posted_by=self.request.user).select_related('posted_by')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PositionCreateUpdateSerializer
        return PositionListSerializer

    def create(self, request, *args, **kwargs):
        """重写create方法，确保正确返回响应"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 使用PositionDetailSerializer返回完整数据
        detail_serializer = PositionDetailSerializer(serializer.instance)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class FacultyPositionUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsFaculty]
    serializer_class = PositionCreateUpdateSerializer
    lookup_field = 'position_id'

    def get_queryset(self):
        return Position.objects.filter(posted_by=self.request.user)


class FacultyPositionClose(APIView):
    permission_classes = [permissions.IsAuthenticated, IsFaculty]

    def patch(self, request, position_id):
        pos = get_object_or_404(Position, position_id=position_id, posted_by=request.user)
        if pos.status != 'open':
            return Response({'detail': '只能关闭开放中的岗位'}, status=400)
        pos.status = 'closed'
        pos.save(update_fields=['status', 'updated_at'])
        return Response({'status': pos.status})


class StudentDashboard(APIView):
    """
    学生看板数据统计
    GET /api/student/dashboard/
    """
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    
    def get(self, request):
        """获取学生看板统计数据"""
        from django.utils import timezone
        from datetime import timedelta
        
        user = request.user
        now = timezone.now()
        
        # 统计可申请岗位数（开放中的岗位且未过期，与列表页面保持一致）
        available_positions = Position.objects.filter(
            status='open',
            application_deadline__gte=now
        ).count()
        
        # 统计申请数据
        applications = Application.objects.filter(applicant=user)
        total_applications = applications.count()
        pending_applications = applications.filter(
            status__in=['submitted', 'reviewing']
        ).count()
        accepted_applications = applications.filter(status='accepted').count()
        rejected_applications = applications.filter(status='rejected').count()
        
        # 获取最近一个月的岗位（最近5条，按创建时间倒序，且未过期）
        one_month_ago = now - timedelta(days=30)
        recent_positions = Position.objects.filter(
            status='open',
            application_deadline__gte=now,
            created_at__gte=one_month_ago
        ).select_related('posted_by').order_by('-created_at')[:5]
        recent_positions_data = PositionListSerializer(
            recent_positions,
            many=True
        ).data
        
        # 获取最近的申请（最近5条，按申请时间倒序）
        recent_applications = applications.select_related(
            'position'
        ).order_by('-applied_at')[:5]
        from application.serializers import ApplicationListSerializer
        recent_applications_data = ApplicationListSerializer(
            recent_applications,
            many=True
        ).data
        
        return Response({
            'statistics': {
                'available_positions': available_positions,
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'accepted_applications': accepted_applications,
                'rejected_applications': rejected_applications,
            },
            'recent_positions': recent_positions_data,
            'recent_applications': recent_applications_data,
        })


class FacultyDashboard(APIView):
    """
    教师看板数据统计
    GET /api/faculty/dashboard/
    """
    permission_classes = [permissions.IsAuthenticated, IsFaculty]
    
    def get(self, request):
        """获取教师看板统计数据"""
        user = request.user
        
        # 统计岗位数据
        positions = Position.objects.filter(posted_by=user)
        total_positions = positions.count()
        open_positions = positions.filter(status='open').count()
        closed_positions = positions.filter(status='closed').count()
        filled_positions = positions.filter(status='filled').count()
        
        # 统计申请数据
        applications = Application.objects.filter(position__posted_by=user)
        total_applications = applications.count()
        pending_applications = applications.filter(
            status__in=['submitted', 'reviewing']
        ).count()
        accepted_applications = applications.filter(status='accepted').count()
        rejected_applications = applications.filter(status='rejected').count()
        
        # 统计在岗助教数（已通过申请的助教）
        active_tas = Application.objects.filter(
            position__posted_by=user,
            status='accepted'
        ).values('applicant').distinct().count()
        
        # 统计待审核工时数
        pending_timesheets = Timesheet.objects.filter(
            position__posted_by=user,
            status='pending'
        ).count()
        
        # 获取最近的岗位（最近3条）
        recent_positions = positions.select_related('posted_by')[:3]
        recent_positions_data = PositionListSerializer(
            recent_positions,
            many=True
        ).data
        
        # 获取最近的申请（最近5条）
        recent_applications = applications.select_related(
            'applicant',
            'position'
        )[:5]
        from application.serializers import ApplicationListSerializer
        recent_applications_data = ApplicationListSerializer(
            recent_applications,
            many=True
        ).data
        
        # 获取最近的待审核工时（最近5条）
        recent_timesheets = Timesheet.objects.filter(
            position__posted_by=user,
            status='pending'
        ).select_related('position', 'ta')[:5]
        from timesheet.serializers import TimesheetListSerializer
        recent_timesheets_data = TimesheetListSerializer(
            recent_timesheets,
            many=True
        ).data
        
        return Response({
            'statistics': {
                'total_positions': total_positions,
                'open_positions': open_positions,
                'closed_positions': closed_positions,
                'filled_positions': filled_positions,
                'total_applications': total_applications,
                'pending_applications': pending_applications,
                'accepted_applications': accepted_applications,
                'rejected_applications': rejected_applications,
                'active_tas': active_tas,
                'pending_timesheets': pending_timesheets,
            },
            'recent_positions': recent_positions_data,
            'recent_applications': recent_applications_data,
            'recent_timesheets': recent_timesheets_data,
        })
