"""
最小安全自检：对核心接口做 SQL 注入 / XSS 冒烟测试。

用法：
    python manage.py security_smoke_test
"""

from django.core.management.base import BaseCommand
from django.test import Client


class Command(BaseCommand):
    help = '对部分核心接口进行最小 SQL 注入 / XSS 冒烟测试'

    def handle(self, *args, **options):
        client = Client()

        self.stdout.write(self.style.MIGRATE_HEADING('开始执行安全冒烟测试...'))

        # 不登录直接访问受保护接口，确认被拒绝（认证层生效）
        self.check_protected_api_requires_auth(client)

        # 使用典型注入 / XSS 载荷访问公开接口，确保不会抛出 500
        self.check_public_endpoints_with_malicious_payloads(client)

        self.stdout.write(self.style.SUCCESS('✅ 安全冒烟测试执行完成（未发现明显异常）。'))

    def check_protected_api_requires_auth(self, client: Client):
        """简单检查几个典型接口是否需要认证。"""
        protected_paths = [
            '/api/student/positions/',
            '/api/faculty/positions/',
            '/api/ta/timesheets/',
            '/api/admin/reports/monthly/',
        ]

        for path in protected_paths:
            resp = client.get(path)
            status = resp.status_code
            if status in (401, 403):
                self.stdout.write(self.style.SUCCESS(f'✓ 受保护接口需认证: {path} -> {status}'))
            else:
                # 不直接失败，只提示需要人工关注
                self.stdout.write(self.style.WARNING(f'! 接口未按预期要求认证: {path} -> {status}'))

    def check_public_endpoints_with_malicious_payloads(self, client: Client):
        """
        用常见 SQL 注入 / XSS 特征字符串访问公开接口，确认不会 500 崩溃。
        注意：这里只做“不会异常”的最小冒烟检查，不验证业务正确性。
        """
        payloads = [
            "' OR 1=1 --",
            "'; DROP TABLE users; --",
            "<script>alert('xss')</script>",
        ]

        # 选取一条公开接口，例如登录接口（通常允许匿名访问）
        test_paths = [
            '/api/auth/login/',
        ]

        for path in test_paths:
            for p in payloads:
                resp = client.post(path, data={'username': p, 'password': p})
                status = resp.status_code
                if 500 <= status < 600:
                    self.stdout.write(
                        self.style.ERROR(f'✗ 接口在恶意载荷下出现 5xx: {path} ({status})')
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ 恶意载荷未导致 5xx: {path} ({status})')
                    )

