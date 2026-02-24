"""
师生聊天 API
- GET/POST /api/chat/conversations/  列表、发起会话
- GET/POST /api/chat/conversations/<id>/messages/  消息列表、发送
"""
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import models

from .models import Conversation, Message
from .serializers import ConversationListSerializer, MessageSerializer, SendMessageSerializer
from recruitment.models import Position
from application.models import Application
from timesheet.models import Timesheet


class ConversationList(ListAPIView):
    """GET /api/chat/conversations/  当前用户参与的会话列表"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConversationListSerializer

    def get_queryset(self):
        return Conversation.objects.filter(
            models.Q(teacher=self.request.user) | models.Q(student=self.request.user)
        ).select_related('teacher', 'student', 'position').order_by('-updated_at')


class StartConversation(APIView):
    """
    POST /api/chat/start/
    body: 其一 { "position_id": 123 } | { "application_id": 456 } | { "timesheet_id": 789 }
    返回会话信息（含 conversation_id）
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        position_id = request.data.get('position_id')
        application_id = request.data.get('application_id')
        timesheet_id = request.data.get('timesheet_id')

        teacher, student, position = None, None, None

        if position_id is not None:
            # 学生从岗位详情发起会话：只要不是该岗位发布教师即可联系
            position = get_object_or_404(Position, position_id=position_id)
            teacher = position.posted_by
            if user == teacher:
                return Response({'detail': '教师请使用 application_id 或 timesheet_id 发起会话'}, status=400)
            student = user
        elif application_id is not None:
            app = get_object_or_404(Application.objects.select_related('position', 'applicant'), application_id=application_id)
            if app.position.posted_by != user:
                return Response({'detail': '无权操作该申请'}, status=403)
            teacher = user
            student = app.applicant
            position = app.position
        elif timesheet_id is not None:
            ts = get_object_or_404(Timesheet.objects.select_related('position', 'ta'), timesheet_id=timesheet_id)
            if ts.position.posted_by != user:
                return Response({'detail': '无权操作该工时'}, status=403)
            teacher = user
            student = ts.ta
            position = ts.position
        else:
            return Response({'detail': '请提供 position_id、application_id 或 timesheet_id'}, status=400)

        conv, _ = Conversation.objects.get_or_create(
            teacher=teacher,
            student=student,
            position=position,
            defaults={}
        )
        conv.save()  # 更新 updated_at
        serializer = ConversationListSerializer(conv, context={'request': request})
        return Response(serializer.data, status=201)


class MessageList(ListAPIView):
    """GET /api/chat/conversations/<conversation_id>/messages/"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        cid = self.kwargs['conversation_id']
        conv = get_object_or_404(Conversation, conversation_id=cid)
        if conv.teacher != self.request.user and conv.student != self.request.user:
            return Message.objects.none()
        return Message.objects.filter(conversation=conv).select_related('sender').order_by('created_at')


class SendMessage(APIView):
    """POST /api/chat/conversations/<conversation_id>/send/  body: { "content": "..." }"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, conversation_id):
        conv = get_object_or_404(Conversation, conversation_id=conversation_id)
        if conv.teacher != request.user and conv.student != request.user:
            return Response({'detail': '无权在此会话发消息'}, status=403)
        ser = SendMessageSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        msg = Message.objects.create(
            conversation=conv,
            sender=request.user,
            content=ser.validated_data['content'],
        )
        conv.updated_at = timezone.now()
        conv.save(update_fields=['updated_at'])
        return Response(MessageSerializer(msg).data, status=201)
