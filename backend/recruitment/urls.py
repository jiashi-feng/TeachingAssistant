from django.urls import path
from .views import (
    StudentPositionList, StudentPositionDetail,
    FacultyPositionListCreate, FacultyPositionUpdate, FacultyPositionClose
)

urlpatterns = [
    path('api/student/positions/', StudentPositionList.as_view(), name='student-position-list'),
    path('api/student/positions/<int:position_id>/', StudentPositionDetail.as_view(), name='student-position-detail'),

    # 教师端
    path('api/faculty/positions/', FacultyPositionListCreate.as_view(), name='faculty-position-list-create'),
    path('api/faculty/positions/<int:position_id>/', FacultyPositionUpdate.as_view(), name='faculty-position-update'),
    path('api/faculty/positions/<int:position_id>/close/', FacultyPositionClose.as_view(), name='faculty-position-close'),
]


