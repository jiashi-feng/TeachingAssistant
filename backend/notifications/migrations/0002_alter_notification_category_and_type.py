# Generated manually for chat notification types

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='category',
            field=models.CharField(
                choices=[
                    ('system', '系统通知'),
                    ('application', '申请相关'),
                    ('timesheet', '工时相关'),
                    ('salary', '薪酬相关'),
                    ('chat', '师生聊天'),
                ],
                max_length=20,
                verbose_name='通知分类',
            ),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(
                choices=[
                    ('system_announcement', '系统公告'),
                    ('system_maintenance', '系统维护通知'),
                    ('account_activated', '账号激活'),
                    ('password_changed', '密码修改'),
                    ('position_published', '新岗位发布'),
                    ('position_updated', '岗位信息更新'),
                    ('position_closed', '岗位关闭'),
                    ('position_deadline_soon', '申请截止提醒'),
                    ('application_submitted', '收到新申请'),
                    ('application_reviewing', '申请审核中'),
                    ('application_accepted', '申请通过'),
                    ('application_rejected', '申请被拒'),
                    ('application_withdrawn', '申请已撤回'),
                    ('timesheet_submitted', '收到工时表'),
                    ('timesheet_approved', '工时已批准'),
                    ('timesheet_rejected', '工时被驳回'),
                    ('timesheet_reminder', '工时提交提醒'),
                    ('salary_generated', '薪酬已生成'),
                    ('salary_paid', '薪酬已发放'),
                    ('salary_delayed', '薪酬延迟通知'),
                    ('role_granted', '角色授予'),
                    ('role_revoked', '角色撤销'),
                    ('became_ta', '成为助教'),
                    ('evaluation_received', '收到工作评价'),
                    ('evaluation_reminder', '评价提醒'),
                    ('chat_new_message', '收到聊天消息'),
                ],
                max_length=50,
                verbose_name='通知类型',
            ),
        ),
    ]
