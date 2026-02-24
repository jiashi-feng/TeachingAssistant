"""
学生助教管理平台 - 师生聊天模块
包含：Conversation（会话表）、Message（消息表）
"""

from django.db import models
from django.conf import settings
from recruitment.models import Position


class Conversation(models.Model):
    """会话表 - 教师与学生/助教的一对一会话，可关联岗位"""
    conversation_id = models.AutoField(primary_key=True, verbose_name='会话ID')
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_conversations',
        verbose_name='教师'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_conversations',
        verbose_name='学生/助教'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversations',
        verbose_name='关联岗位'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'conversation'
        verbose_name = '会话'
        verbose_name_plural = '会话'
        ordering = ['-updated_at']
        unique_together = [['teacher', 'student', 'position']]
        indexes = [
            models.Index(fields=['teacher']),
            models.Index(fields=['student']),
            models.Index(fields=['updated_at']),
        ]

    def __str__(self):
        return f'{self.teacher.real_name} - {self.student.real_name}'


class Message(models.Model):
    """消息表"""
    message_id = models.AutoField(primary_key=True, verbose_name='消息ID')
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='会话'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        verbose_name='发送者'
    )
    content = models.TextField(verbose_name='内容')
    is_read = models.BooleanField(default=False, verbose_name='已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='已读时间')

    class Meta:
        db_table = 'message'
        verbose_name = '消息'
        verbose_name_plural = '消息'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.sender.real_name}: {self.content[:20]}'
