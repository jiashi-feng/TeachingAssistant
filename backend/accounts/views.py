"""
学生助教管理平台 - 用户认证模块视图

实现用户注册、登录、登出、个人信息管理等功能
"""

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer
)


# ==============================================================================
# JWT Token 视图
# ==============================================================================

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    自定义JWT Token获取视图
    POST /api/auth/token/
    返回access_token、refresh_token和用户完整信息
    """
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    JWT Token刷新视图
    POST /api/auth/token/refresh/
    """
    pass


# ==============================================================================
# 用户认证视图
# ==============================================================================

class RegisterView(APIView):
    """
    用户注册接口
    POST /api/auth/register/
    
    支持学生、教师、管理员三种角色的注册
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # 生成JWT Token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': '注册成功',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': '注册失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    用户登录接口
    POST /api/auth/login/
    
    返回JWT Token和用户信息
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # 更新最后登录时间
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # 生成JWT Token
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': '登录成功',
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': '登录失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    用户登出接口
    POST /api/auth/logout/
    
    将refresh_token加入黑名单
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # 同时兼容 refresh_token 与 refresh 两种字段，提升前后端兼容性
        refresh_token = request.data.get('refresh_token') or request.data.get('refresh')

        if not refresh_token:
            return Response({
                'message': '缺少refresh_token'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 将token加入黑名单；若token无效或已失效/已拉黑，也视为幂等成功
        try:
            token = RefreshToken(refresh_token)
            try:
                token.blacklist()
            except Exception:
                # 已失效/已拉黑等情况，视为登出成功（幂等）
                pass
            return Response({'message': '登出成功'}, status=status.HTTP_200_OK)
        except TokenError:
            # 无效的refresh token，同样视为登出成功（幂等）
            return Response({'message': '登出成功'}, status=status.HTTP_200_OK)
        except Exception as e:
            # 其他异常不应影响前端登出体验，也返回成功
            return Response({'message': '登出成功'}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    """
    获取当前用户信息
    GET /api/auth/profile/
    
    返回当前登录用户的完整信息
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        
        return Response({
            'message': '获取用户信息成功',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request):
        """
        更新用户基本信息
        PUT /api/auth/profile/
        """
        user = request.user
        
        # 允许更新的字段
        allowed_fields = ['real_name', 'phone', 'email']
        
        for field in allowed_fields:
            if field in request.data:
                setattr(user, field, request.data[field])
        
        try:
            user.save()
            return Response({
                'message': '更新成功',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'message': '更新失败',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    修改密码接口
    PUT /api/auth/change-password/
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'message': '密码修改成功，请重新登录'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': '密码修改失败',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    """
    用户列表接口（管理员使用）
    GET /api/auth/users/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_queryset(self):
        """支持搜索和筛选"""
        queryset = User.objects.all().order_by('-created_at')
        
        # 搜索
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                real_name__icontains=search
            ) | queryset.filter(
                email__icontains=search
            )
        
        # 按角色筛选
        role_code = self.request.query_params.get('role', None)
        if role_code:
            queryset = queryset.filter(
                userrole__role__role_code=role_code
            ).distinct()
        
        # 按激活状态筛选
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset


class UserDetailView(generics.RetrieveAPIView):
    """
    用户详情接口
    GET /api/auth/users/{user_id}/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'user_id'


# ==============================================================================
# 辅助视图
# ==============================================================================

class CheckUsernameView(APIView):
    """
    检查用户名是否可用
    GET /api/auth/check-username/?username=xxx
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        username = request.query_params.get('username', None)
        
        if not username:
            return Response({
                'message': '请提供用户名'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        exists = User.objects.filter(username=username).exists()
        
        return Response({
            'available': not exists,
            'message': '用户名已存在' if exists else '用户名可用'
        }, status=status.HTTP_200_OK)


class CheckEmailView(APIView):
    """
    检查邮箱是否可用
    GET /api/auth/check-email/?email=xxx
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        email = request.query_params.get('email', None)
        
        if not email:
            return Response({
                'message': '请提供邮箱'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        exists = User.objects.filter(email=email).exists()
        
        return Response({
            'available': not exists,
            'message': '邮箱已注册' if exists else '邮箱可用'
        }, status=status.HTTP_200_OK)



class CheckUserIdView(APIView):
    """
    检查用户ID是否可用
    GET /api/auth/check-user-id/?user_id=xxx
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        user_id = request.query_params.get('user_id', None)
        
        if not user_id:
            return Response({
                'message': '请提供用户ID'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        exists = User.objects.filter(user_id=user_id).exists()
        
        return Response({
            'available': not exists,
            'message': '用户ID已存在' if exists else '用户ID可用'
        }, status=status.HTTP_200_OK)
