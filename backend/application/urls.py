from django.urls import path
from .views import SubmitApplication, MyApplications, MyApplicationDetail, PositionApplications, ReviewApplication, RevokeApplicationReview

urlpatterns = [
    # 学生端
    path('api/student/applications/submit/', SubmitApplication.as_view(), name='student-application-submit'),
    path('api/student/applications/', MyApplications.as_view(), name='student-application-list'),
    path('api/student/applications/<int:application_id>/', MyApplicationDetail.as_view(), name='student-application-detail'),

    # 教师端
    path('api/faculty/positions/<int:position_id>/applications/', PositionApplications.as_view(), name='faculty-position-applications'),
    path('api/faculty/applications/<int:application_id>/review/', ReviewApplication.as_view(), name='faculty-application-review'),
    path('api/faculty/applications/<int:application_id>/revoke/', RevokeApplicationReview.as_view(), name='faculty-application-revoke'),
]


