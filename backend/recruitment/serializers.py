from rest_framework import serializers
from .models import Position


class PositionListSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.CharField(source='posted_by.real_name', read_only=True)

    class Meta:
        model = Position
        fields = [
            'position_id', 'title', 'course_name', 'course_code', 'application_deadline',
            'status', 'posted_by', 'posted_by_name', 'num_positions', 'num_filled', 'created_at'
        ]
        read_only_fields = fields


class PositionDetailSerializer(serializers.ModelSerializer):
    posted_by_name = serializers.CharField(source='posted_by.real_name', read_only=True)

    class Meta:
        model = Position
        fields = [
            'position_id', 'title', 'course_name', 'course_code', 'description',
            'requirements', 'num_positions', 'num_filled', 'work_hours_per_week',
            'hourly_rate', 'start_date', 'end_date', 'application_deadline',
            'status', 'posted_by', 'posted_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = fields


class PositionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = [
            'title', 'course_name', 'course_code', 'description', 'requirements',
            'num_positions', 'work_hours_per_week', 'hourly_rate',
            'start_date', 'end_date', 'application_deadline'
        ]

    def validate(self, attrs):
        start = attrs.get('start_date')
        end = attrs.get('end_date')
        if start and end and start > end:
            raise serializers.ValidationError('开始日期不能晚于结束日期')
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Position.objects.create(posted_by=user, **validated_data)

