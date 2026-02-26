"""
TeachingAssistant 项目后端 API 冒烟测试脚本

用途：
    - 快速验证后端在本地启动后，核心接口是否可用
    - 覆盖登录、学生岗位/申请、教师审核、管理端报表等基础链路

使用方法：
    1. 确保后端已在本地运行： http://localhost:8000
    2. 确保已执行过测试数据命令： python manage.py create_test_data
    3. 在项目根目录执行：
         python scripts/api_smoke_test.py
"""

import sys
from typing import Optional, Dict, Any

import requests


BASE_URL = "http://localhost:8000"


TEST_USERS = {
    "student": {"username": "student1", "password": "password123"},
    "teacher": {"username": "teacher1", "password": "password123"},
    "admin": {"username": "admin", "password": "password123"},
}


def api_request(
    method: str,
    path: str,
    token: Optional[str] = None,
    **kwargs: Any,
) -> Optional[requests.Response]:
    url = BASE_URL.rstrip("/") + path
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.request(method, url, headers=headers, timeout=10, **kwargs)
        return resp
    except Exception as e:
        print(f"[ERROR] 请求失败 {method} {url}: {e}")
        return None


def login(user_type: str) -> Optional[str]:
    creds = TEST_USERS[user_type]
    print(f"\n== 尝试登录 {user_type} 用户: {creds['username']} ==")
    resp = api_request(
        "POST",
        "/api/auth/login/",
        json={"username": creds["username"], "password": creds["password"]},
    )
    if resp is None:
        return None
    print(f"[login] status={resp.status_code}")
    if resp.status_code != 200:
        print(f"[login] 登录失败，响应：{resp.text}")
        return None
    data = resp.json()
    token = (
    data.get("tokens", {}).get("access")
    or data.get("data", {}).get("tokens", {}).get("access")  
)
    if not token:
        print("[login] 未在响应中找到 access token")
        return None
    return token


def check_student_flow(token: str) -> None:
    print("\n== 学生端冒烟测试 ==")

    # 1. 岗位列表
    resp = api_request("GET", "/api/student/positions/", token=token, params={"page": 1})
    if resp:
        print(f"[student positions] status={resp.status_code}, count={len(resp.json().get('results', [])) if resp.status_code == 200 else 'N/A'}")

    # 2. 我的申请列表
    resp = api_request("GET", "/api/student/applications/", token=token)
    if resp:
        print(f"[student applications] status={resp.status_code}")


def check_teacher_flow(token: str) -> None:
    print("\n== 教师端冒烟测试 ==")

    # 1. 我的岗位列表
    resp = api_request("GET", "/api/faculty/positions/", token=token)
    if resp:
        print(f"[faculty positions] status={resp.status_code}")

    # 2. 工时审核列表
    resp = api_request("GET", "/api/faculty/timesheets/", token=token)
    if resp:
        print(f"[faculty timesheets] status={resp.status_code}")


def check_admin_flow(token: str) -> None:
    print("\n== 管理端冒烟测试 ==")

    # 1. 本月报表
    resp = api_request("GET", "/api/admin/reports/monthly/", token=token)
    if resp:
        print(f"[admin monthly report] status={resp.status_code}")

    # 2. 趋势接口（默认参数）
    resp = api_request(
        "GET",
        "/api/admin/reports/trends/",
        token=token,
        params={"metric": "applications", "group_by": "year"},
    )
    if resp:
        print(f"[admin trends] status={resp.status_code}")


def main() -> int:
    print("=== TeachingAssistant API 冒烟测试开始 ===")
    print(f"后端地址：{BASE_URL}")

    # 学生
    student_token = login("student")
    if student_token:
        check_student_flow(student_token)
    else:
        print("[warn] 学生登录失败，跳过学生端冒烟测试。")

    # 教师
    teacher_token = login("teacher")
    if teacher_token:
        check_teacher_flow(teacher_token)
    else:
        print("[warn] 教师登录失败，跳过教师端冒烟测试。")

    # 管理员
    admin_token = login("admin")
    if admin_token:
        check_admin_flow(admin_token)
    else:
        print("[warn] 管理员登录失败，跳过管理端冒烟测试。")

    print("\n=== TeachingAssistant API 冒烟测试结束 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())

