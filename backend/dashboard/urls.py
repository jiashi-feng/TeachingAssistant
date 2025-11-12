"""
学生助教管理平台 - 数据看板模块URL配置
"""

from django.urls import path
from .views import MonthlyReport

app_name = 'dashboard'

urlpatterns = [
    path('api/admin/reports/monthly/', MonthlyReport.as_view(), name='monthly-report'),
]

