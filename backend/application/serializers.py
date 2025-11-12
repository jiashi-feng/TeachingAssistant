from django.conf import settings
from rest_framework import serializers
from .models import Application
from recruitment.models import Position


class ApplicationCreateSerializer(serializers.ModelSerializer):
    resume_text = serializers.CharField(required=False, allow_blank=True, trim_whitespace=False)
    resume = serializers.FileField(required=False, allow_null=True)
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())

    class Meta:
        model = Application
        fields = ['position', 'resume_text', 'resume']

    def validate(self, attrs):
        from django.utils import timezone
        
        request = self.context['request']
        user = request.user
        position = attrs.get('position')
        has_text = bool(attrs.get('resume_text'))
        has_file = bool(attrs.get('resume'))

        # 必须二选一
        if not (has_text ^ has_file):
            raise serializers.ValidationError('请在"在线填写"和"上传简历文件"中二选一。')

        # 检查岗位状态
        if position.status != 'open':
            raise serializers.ValidationError('该岗位已关闭，无法申请。')
        
        # 检查申请截止时间
        now = timezone.now()
        if position.application_deadline < now:
            raise serializers.ValidationError('该岗位申请已过期，无法申请。')

        # 同一岗位唯一申请
        if Application.objects.filter(position=position, applicant=user).exists():
            raise serializers.ValidationError('您已申请过该岗位。')

        # 文件校验
        f = attrs.get('resume')
        if f:
            if f.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise serializers.ValidationError('文件过大，请控制在10MB以内。')
            if hasattr(f, 'content_type') and f.content_type not in getattr(settings, 'ALLOWED_DOCUMENT_TYPES', []):
                raise serializers.ValidationError('仅支持上传 pdf/doc/docx 格式。')

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Application.objects.create(applicant=user, status='submitted', **validated_data)


class ApplicationListSerializer(serializers.ModelSerializer):
    position_title = serializers.CharField(source='position.title', read_only=True)
    applicant_name = serializers.CharField(source='applicant.real_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Application
        fields = [
            'application_id',
            'position',
            'position_title',
            'applicant',
            'applicant_name',
            'status',
            'status_display',
            'applied_at',
        ]
        read_only_fields = fields


class ApplicationDetailSerializer(serializers.ModelSerializer):
    position_title = serializers.CharField(source='position.title', read_only=True)

    class Meta:
        model = Application
        fields = [
            'application_id', 'position', 'position_title', 'status',
            'resume', 'resume_text', 'applied_at', 'reviewed_at', 'review_notes'
        ]
        read_only_fields = fields


