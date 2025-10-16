"""
学生助教管理平台 - 用户认证模块URL配置
"""

from django.urls import path
from .views import (
    # JWT Token
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    
    # 用户认证
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    ChangePasswordView,
    
    # 用户管理
    UserListView,
    UserDetailView,
    
    # 辅助接口
    CheckUsernameView,
    CheckEmailView,
)

app_name = 'accounts'

urlpatterns = [
    # ==============================================================================
    # JWT Token相关
    # ==============================================================================
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    # ==============================================================================
    # 用户认证
    # ==============================================================================
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # ==============================================================================
    # 用户管理
    # ==============================================================================
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<str:user_id>/', UserDetailView.as_view(), name='user_detail'),
    
    # ==============================================================================
    # 辅助接口
    # ==============================================================================
    path('check-username/', CheckUsernameView.as_view(), name='check_username'),
    path('check-email/', CheckEmailView.as_view(), name='check_email'),
]

