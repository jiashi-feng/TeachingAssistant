"""
学生助教管理平台 - 数据看板模块URL配置
"""

from django.urls import path
from .views import MonthlyReport, MonthlyReportExport, TrendsReport

app_name = 'dashboard'

urlpatterns = [
    path('api/admin/reports/monthly/', MonthlyReport.as_view(), name='monthly-report'),
    path('api/admin/reports/export/', MonthlyReportExport.as_view(), name='monthly-export'),
    path('api/admin/reports/trends/', TrendsReport.as_view(), name='trends-report'),
]

