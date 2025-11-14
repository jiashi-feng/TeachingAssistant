from rest_framework import generics, permissions, parsers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from accounts.permissions import IsStudent, IsFaculty
from accounts.models import Student
from .models import Application
from .serializers import (
    ApplicationCreateSerializer,
    ApplicationListSerializer,
    ApplicationDetailSerializer,
)
from recruitment.models import Position
from django.utils import timezone
from django.db import transaction
from rest_framework.decorators import api_view
from notifications.models import Notification


class SubmitApplication(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]

    def post(self, request):
        serializer = ApplicationCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        app = serializer.save()
        return Response(ApplicationDetailSerializer(app).data, status=201)


class MyApplications(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = ApplicationListSerializer

    def get_queryset(self):
        queryset = Application.objects.filter(applicant=self.request.user).select_related('position')
        
        # 支持按状态筛选
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset


class MyApplicationDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = ApplicationDetailSerializer
    lookup_field = 'application_id'

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user).select_related('position')


class PositionApplications(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsFaculty]
    serializer_class = ApplicationListSerializer

    def get_queryset(self):
        position_id = self.kwargs.get('position_id')
        position = get_object_or_404(Position, position_id=position_id, posted_by=self.request.user)
        return Application.objects.filter(position=position).select_related('position', 'applicant')

class FacultyApplications(generics.ListAPIView):
    permission_classes= [permissions.IsAuthenticated, IsFaculty]
    serializer_class = ApplicationListSerializer

    def get_queryset(self):
        
        queryset = Application.objects.filter(
            position__posted_by=self.request.user
        ).select_related('position', 'applicant')

        # 支持按状态筛选
        status =self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        # 支持按申请时间排序
        ordering = self.request.query_params.get('ordering', '-applied_at')
        if ordering:
            queryset =queryset.order_by(ordering)

        return queryset


class ReviewApplication(APIView):
    permission_classes = [permissions.IsAuthenticated, IsFaculty]

    def post(self, request, application_id):
        app = get_object_or_404(Application.objects.select_related('position'), application_id=application_id)
        # 仅岗位发布者可审核
        if app.position.posted_by != request.user:
            return Response({'detail': '无权审核该申请'}, status=403)

        action = request.data.get('action')
        if action not in ['accept', 'reject']:
            return Response({'detail': 'action 取值应为 accept 或 reject'}, status=400)

        # 终结状态不可再变更（高校平台常规机制）
        if app.status in ['accepted', 'rejected']:
            return Response({'detail': '该申请已审核完成，无法再次变更'}, status=400)

        with transaction.atomic():
            # 刷新应用状态，防止并发覆盖
            app = Application.objects.select_for_update().select_related('position').get(application_id=application_id)
            pos = app.position

            if action == 'accept':
                # 防止超额录用
                if pos.num_filled >= pos.num_positions:
                    return Response({'detail': '该岗位已招满，无法再录用'}, status=400)
                pos.num_filled = pos.num_filled + 1
                # 保存岗位以触发 Position.save 中的状态联动（可能变为 filled）
                pos.save(update_fields=['num_filled', 'updated_at', 'status'])
                app.status = 'accepted'
                
                # 更新学生的助教状态
                try:
                    student = Student.objects.get(user=app.applicant)
                    if not student.is_ta:
                        student.is_ta = True
                        student.ta_since = timezone.now().date()
                        student.save(update_fields=['is_ta', 'ta_since', 'updated_at'])
                except Student.DoesNotExist:
                    pass  # 如果不是学生，跳过
            else:
                app.status = 'rejected'

            app.reviewed_at = timezone.now()
            app.reviewed_by = request.user
            app.review_notes = request.data.get('notes') or app.review_notes
            app.save(update_fields=['status', 'reviewed_at', 'reviewed_by', 'review_notes', 'updated_at'])

        return Response({'status': app.status})


class RevokeApplicationReview(APIView):
    """
    教师撤销审核：将 accepted/rejected 撤销为 reviewing；
    若原为 accepted，需相应减少岗位 num_filled（>=0保护）。
    """
    permission_classes = [permissions.IsAuthenticated, IsFaculty]

    def post(self, request, application_id):
        with transaction.atomic():
            app = get_object_or_404(Application.objects.select_for_update().select_related('position'), application_id=application_id)
            if app.position.posted_by != request.user:
                return Response({'detail': '无权撤销该申请'}, status=403)

            if app.status not in ['accepted', 'rejected']:
                return Response({'detail': '仅已审核的申请可撤销'}, status=400)

            pos = app.position
            was_accepted = app.status == 'accepted'
            
            if was_accepted and pos.num_filled > 0:
                pos.num_filled = pos.num_filled - 1
                pos.save(update_fields=['num_filled', 'updated_at', 'status'])
                
                # 检查该学生是否还有其他已通过的申请
                # 如果没有，则取消助教身份
                other_accepted_apps = Application.objects.filter(
                    applicant=app.applicant,
                    status='accepted'
                ).exclude(application_id=app.application_id)
                
                if not other_accepted_apps.exists():
                    # 没有其他已通过的申请，取消助教身份
                    try:
                        student = Student.objects.get(user=app.applicant)
                        if student.is_ta:
                            student.is_ta = False
                            student.ta_since = None
                            student.save(update_fields=['is_ta', 'ta_since', 'updated_at'])
                    except Student.DoesNotExist:
                        pass  # 如果不是学生，跳过

            app.status = 'reviewing'
            app.reviewed_at = None
            app.reviewed_by = None
            # 保留 review_notes 作为历史备注，或按需清空：这里选择保留
            app.save(update_fields=['status', 'reviewed_at', 'reviewed_by', 'updated_at'])

            # 发送撤销通知（使用已定义的 application_reviewing 类型）
            Notification.objects.create(
                recipient=app.applicant,
                sender=request.user,
                notification_type='application_reviewing',
                category='application',
                title='审核已撤销',
                message=f'您对“{pos.title}”的申请审核已撤销，状态回到审核中。',
                related_model='Application',
                related_object_id=app.application_id,
                priority='medium',
            )

            return Response({'status': app.status})
