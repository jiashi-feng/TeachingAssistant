"""
学生助教管理平台 - 主URL配置

路由规范：
- /admin/ - Django管理后台
- /api/auth/ - 用户认证相关接口
- /api/student/ - 学生端接口
- /api/faculty/ - 教师端接口
- /api/ta/ - 助教端接口
- /api/admin/ - 管理员端接口
- /api/notifications/ - 通知接口
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ==============================================================================
    # Django管理后台
    # ==============================================================================
    path('admin/', admin.site.urls),
    
    # ==============================================================================
    # API接口
    # ==============================================================================
    
    # 用户认证模块
    path('api/auth/', include('accounts.urls')),
    
    # 招募管理模块（教师端）- 第四阶段实现
    # path('api/faculty/', include('recruitment.urls')),
    
    # 申请管理模块（学生端）- 第四阶段实现
    # path('api/student/', include('application.urls')),
    
    # 工时管理模块（助教端）- 第四阶段实现
    # path('api/ta/', include('timesheet.urls')),
    
    # 数据看板模块（管理员端）- 第四阶段实现
    # path('api/admin/', include('dashboard.urls')),
    
    # 通知模块 - 第四阶段实现
    # path('api/notifications/', include('notifications.urls')),
]

# ==============================================================================
# 开发环境：静态文件和媒体文件服务
# ==============================================================================
if settings.DEBUG:
    # 媒体文件（用户上传）
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # 静态文件
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# ==============================================================================
# 自定义Admin站点信息
# ==============================================================================
admin.site.site_header = '学生助教管理平台'
admin.site.site_title = '助教管理系统'
admin.site.index_title = '欢迎使用学生助教管理平台'
