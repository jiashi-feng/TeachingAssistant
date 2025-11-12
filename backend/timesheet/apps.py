from django.apps import AppConfig


class TimesheetConfig(AppConfig):
    name = 'timesheet'
    
    def ready(self):
        # 注册信号
        from . import signals  # noqa