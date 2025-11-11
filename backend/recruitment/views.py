from rest_framework import generics, permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import IsStudent, IsFaculty
from .models import Position
from .serializers import PositionListSerializer, PositionDetailSerializer, PositionCreateUpdateSerializer


class StudentPositionList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]
    serializer_class = PositionListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'course_code', 'posted_by']
    search_fields = ['title', 'course_name', 'description']
    ordering_fields = ['application_deadline', 'created_at']

    def get_queryset(self):
        return Position.objects.filter(status='open').select_related('posted_by')


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
