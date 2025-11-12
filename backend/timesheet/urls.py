"""
学生助教管理平台 - 工时管理模块URL配置
"""

from django.urls import path
from .views import (
    TimesheetListCreate,
    MyTimesheetDetail,
    UpdateTimesheet,
    MySalaries,
    SalaryDetail,
    TADashboard,
    FacultyTimesheetList,
    FacultyTimesheetDetail,
    ReviewTimesheet,
)

app_name = 'timesheet'

urlpatterns = [
    # 工时管理
    path('api/ta/timesheets/', TimesheetListCreate.as_view(), name='timesheet-list-create'),
    path('api/ta/timesheets/<int:timesheet_id>/', MyTimesheetDetail.as_view(), name='timesheet-detail'),
    path('api/ta/timesheets/<int:timesheet_id>/update/', UpdateTimesheet.as_view(), name='update-timesheet'),
    
    # 薪酬查询
    path('api/ta/salaries/', MySalaries.as_view(), name='my-salaries'),
    path('api/ta/salaries/<int:salary_id>/', SalaryDetail.as_view(), name='salary-detail'),
    
    # 助教看板
    path('api/ta/dashboard/', TADashboard.as_view(), name='ta-dashboard'),
    
    # 教师端工时审核
    path('api/faculty/timesheets/', FacultyTimesheetList.as_view(), name='faculty-timesheet-list'),
    path('api/faculty/timesheets/<int:timesheet_id>/', FacultyTimesheetDetail.as_view(), name='faculty-timesheet-detail'),
    path('api/faculty/timesheets/<int:timesheet_id>/review/', ReviewTimesheet.as_view(), name='review-timesheet'),
]

