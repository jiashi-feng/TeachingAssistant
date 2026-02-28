"""
自定义中间件
- 对 /api/ 路径豁免 CSRF 检查（JWT API 无需 session cookie，CSRF 不适用）
"""

from django.middleware.csrf import CsrfViewMiddleware


class ApiCsrfExemptMiddleware(CsrfViewMiddleware):
    """
    继承 Django 的 CsrfViewMiddleware，对 /api/ 路径跳过 CSRF 检查。
    用于前后端同域部署时，前端静态文件不经过 Django，无法设置 CSRF cookie 的情况。
    """

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if request.path.startswith('/api/'):
            return None  # 跳过 CSRF 检查
        return super().process_view(request, callback, callback_args, callback_kwargs)
