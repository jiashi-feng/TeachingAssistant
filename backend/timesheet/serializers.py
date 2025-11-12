"""
学生助教管理平台 - 工时管理模块序列化器
包含：工时表序列化器、薪酬记录序列化器
"""

from rest_framework import serializers
from .models import Timesheet, Salary
from recruitment.models import Position
from application.models import Application
from datetime import datetime


class TimesheetCreateSerializer(serializers.ModelSerializer):
    """工时表创建序列化器"""
    month = serializers.DateField(
        input_formats=['%Y-%m-%d'],
        help_text='工作月份，格式：YYYY-MM-DD（月初日期，如：2025-03-01）'
    )
    position = serializers.PrimaryKeyRelatedField(
        queryset=Position.objects.all(),
        help_text='岗位ID'
    )
    
    class Meta:
        model = Timesheet
        fields = ['position', 'month', 'hours_worked', 'work_description']
    
    def validate(self, attrs):
        """验证业务逻辑"""
        request = self.context['request']
        user = request.user
        position = attrs.get('position')
        month = attrs.get('month')
        
        # 验证：必须是已通过的申请对应的岗位
        if not Application.objects.filter(
            applicant=user,
            position=position,
            status='accepted'
        ).exists():
            raise serializers.ValidationError({
                'position': '您不是该岗位的助教，无法提交工时表'
            })
        
        # 验证：同一岗位同一月份不能重复提交
        if Timesheet.objects.filter(
            ta=user,
            position=position,
            month=month
        ).exists():
            raise serializers.ValidationError({
                'month': '该月份工时表已提交，无法重复提交'
            })
        
        # 验证：月份不能是未来月份
        today = datetime.now().date()
        if month > today:
            raise serializers.ValidationError({
                'month': '不能提交未来月份的工时表'
            })
        
        return attrs
    
    def create(self, validated_data):
        """创建工时表"""
        # 修复：从 context 中获取 request.user，而不是从 perform_create 传递
        # 这样可以避免参数传递冲突
        user = self.context['request'].user
        return Timesheet.objects.create(
            ta=user,
            status='pending',
            **validated_data
        )


class TimesheetUpdateSerializer(serializers.ModelSerializer):
    """工时表更新序列化器（仅限待审核状态）"""
    month = serializers.DateField(
        input_formats=['%Y-%m-%d'],
        required=False,
        help_text='工作月份，格式：YYYY-MM-DD'
    )
    
    class Meta:
        model = Timesheet
        fields = ['month', 'hours_worked', 'work_description']
    
    def validate(self, attrs):
        """验证：只能编辑待审核状态的工时表"""
        instance = self.instance
        if instance.status != 'pending':
            raise serializers.ValidationError('只能编辑待审核状态的工时表')
        
        # 如果修改了月份，需要检查是否重复
        month = attrs.get('month')
        if month and month != instance.month:
            if Timesheet.objects.filter(
                ta=instance.ta,
                position=instance.position,
                month=month
            ).exclude(timesheet_id=instance.timesheet_id).exists():
                raise serializers.ValidationError({
                    'month': '该月份工时表已存在'
                })
        
        return attrs


class TimesheetListSerializer(serializers.ModelSerializer):
    """工时表列表序列化器"""
    position_title = serializers.SerializerMethodField()
    position_course_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    month_display = serializers.SerializerMethodField()
    ta_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Timesheet
        fields = [
            'timesheet_id',
            'position',
            'position_title',
            'position_course_name',
            'ta',
            'ta_name',
            'month',
            'month_display',
            'hours_worked',
            'work_description',
            'status',
            'status_display',
            'submitted_at',
            'reviewed_by',
            'reviewed_by_name',
            'reviewed_at',
            'review_notes',
        ]
    
    def get_month_display(self, obj):
        """格式化月份显示"""
        # 使用自定义格式化避免 Windows locale 编码问题
        return f"{obj.month.year}年{obj.month.month:02d}月"
    
    def get_position_title(self, obj):
        """获取岗位标题（安全处理 None）"""
        return obj.position.title if obj.position else None
    
    def get_position_course_name(self, obj):
        """获取岗位课程名称（安全处理 None）"""
        return obj.position.course_name if obj.position else None
    
    def get_ta_name(self, obj):
        """获取助教姓名（安全处理 None）"""
        return obj.ta.real_name if obj.ta else None
    
    def get_reviewed_by_name(self, obj):
        """获取审核人姓名，安全处理 None 值"""
        return obj.reviewed_by.real_name if obj.reviewed_by else None


class TimesheetDetailSerializer(serializers.ModelSerializer):
    """工时表详情序列化器"""
    position_title = serializers.CharField(
        source='position.title',
        read_only=True
    )
    position_course_name = serializers.CharField(
        source='position.course_name',
        read_only=True
    )
    position_course_code = serializers.CharField(
        source='position.course_code',
        read_only=True
    )
    position_hourly_rate = serializers.DecimalField(
        source='position.hourly_rate',
        max_digits=8,
        decimal_places=2,
        read_only=True
    )
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    month_display = serializers.SerializerMethodField()
    ta_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    calculated_salary = serializers.SerializerMethodField()
    has_salary = serializers.SerializerMethodField()
    
    class Meta:
        model = Timesheet
        fields = [
            'timesheet_id',
            'ta',
            'ta_name',
            'position',
            'position_title',
            'position_course_name',
            'position_course_code',
            'position_hourly_rate',
            'month',
            'month_display',
            'hours_worked',
            'work_description',
            'status',
            'status_display',
            'submitted_at',
            'reviewed_by',
            'reviewed_by_name',
            'reviewed_at',
            'review_notes',
            'created_at',
            'updated_at',
            'calculated_salary',
            'has_salary',
        ]
    
    def get_month_display(self, obj):
        """格式化月份显示"""
        return f"{obj.month.year}年{obj.month.month:02d}月"
    
    def get_ta_name(self, obj):
        """获取助教姓名"""
        return obj.ta.real_name if obj.ta else None
    
    def get_calculated_salary(self, obj):
        """计算薪酬金额"""
        if obj.status == 'approved':
            return float(obj.calculate_salary())
        return None
    
    def get_has_salary(self, obj):
        """检查是否已生成薪酬记录"""
        return hasattr(obj, 'salary')
    
    def get_reviewed_by_name(self, obj):
        """获取审核人姓名"""
        return obj.reviewed_by.real_name if obj.reviewed_by else None


class SalaryListSerializer(serializers.ModelSerializer):
    """薪酬记录列表序列化器"""
    timesheet_month = serializers.SerializerMethodField()
    position_title = serializers.CharField(
        source='timesheet.position.title',
        read_only=True
    )
    position_course_name = serializers.CharField(
        source='timesheet.position.course_name',
        read_only=True
    )
    payment_status_display = serializers.CharField(
        source='get_payment_status_display',
        read_only=True
    )
    generated_by_name = serializers.CharField(
        source='generated_by.real_name',
        read_only=True
    )
    
    class Meta:
        model = Salary
        fields = [
            'salary_id',
            'timesheet',
            'timesheet_month',
            'position_title',
            'position_course_name',
            'amount',
            'calculation_details',
            'payment_status',
            'payment_status_display',
            'generated_by',
            'generated_by_name',
            'generated_at',
            'paid_at',
            'payment_method',
            'transaction_id',
        ]
    
    def get_timesheet_month(self, obj):
        """格式化月份显示"""
        return f"{obj.timesheet.month.year}年{obj.timesheet.month.month:02d}月"


class TimesheetReviewSerializer(serializers.Serializer):
    """工时审核序列化器"""
    action = serializers.ChoiceField(
        choices=['approve', 'reject'],
        help_text='审核操作：approve（批准）或 reject（驳回）'
    )
    review_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='审核备注'
    )


class SalaryDetailSerializer(serializers.ModelSerializer):
    """薪酬记录详情序列化器"""
    timesheet_month = serializers.SerializerMethodField()
    timesheet_hours = serializers.DecimalField(
        source='timesheet.hours_worked',
        max_digits=5,
        decimal_places=2,
        read_only=True
    )
    timesheet_description = serializers.CharField(
        source='timesheet.work_description',
        read_only=True
    )
    position_title = serializers.CharField(
        source='timesheet.position.title',
        read_only=True
    )
    position_course_name = serializers.CharField(
        source='timesheet.position.course_name',
        read_only=True
    )
    position_course_code = serializers.CharField(
        source='timesheet.position.course_code',
        read_only=True
    )
    position_hourly_rate = serializers.DecimalField(
        source='timesheet.position.hourly_rate',
        max_digits=8,
        decimal_places=2,
        read_only=True
    )
    ta_name = serializers.CharField(
        source='timesheet.ta.real_name',
        read_only=True
    )
    payment_status_display = serializers.CharField(
        source='get_payment_status_display',
        read_only=True
    )
    generated_by_name = serializers.CharField(
        source='generated_by.real_name',
        read_only=True
    )
    
    class Meta:
        model = Salary
        fields = [
            'salary_id',
            'timesheet',
            'timesheet_month',
            'timesheet_hours',
            'timesheet_description',
            'position_title',
            'position_course_name',
            'position_course_code',
            'position_hourly_rate',
            'ta_name',
            'amount',
            'calculation_details',
            'payment_status',
            'payment_status_display',
            'generated_by',
            'generated_by_name',
            'generated_at',
            'paid_at',
            'payment_method',
            'transaction_id',
            'created_at',
            'updated_at',
        ]
    
    def get_timesheet_month(self, obj):
        """格式化月份显示"""
        return f"{obj.timesheet.month.year}年{obj.timesheet.month.month:02d}月"


class TimesheetReviewSerializer(serializers.Serializer):
    """工时审核序列化器"""
    action = serializers.ChoiceField(
        choices=['approve', 'reject'],
        help_text='审核操作：approve（批准）或 reject（驳回）'
    )
    review_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='审核备注'
    )

