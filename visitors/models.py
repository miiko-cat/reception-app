import uuid
from django.db import models
from django.utils import timezone


class Visitor(models.Model):
  id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False,
    verbose_name='主キー'
  )
  visitor_name = models.CharField(
    max_length=100,
    verbose_name='来訪者名'
  )
  visit_purpose = models.CharField(
    max_length=255,
    verbose_name='来訪目的'
  )
  phone_number = models.CharField(
    max_length=20,
    null=True,
    blank=True,
    verbose_name='電話番号'
  )
  email = models.CharField(
    max_length=255,
    null=True,
    blank=True,
    verbose_name='メールアドレス'
  )
  checked_in_at = models.DateTimeField(
    default=timezone.now,
    verbose_name='受付日時'
  )
  checked_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='作成日時'
  )
  deleted_at = models.DateTimeField(
    null=True,
    blank=True,
    verbose_name='更新日時'
  )
  is_deleted = models.BooleanField(
    default=False,
    verbose_name='論理削除'
  )
  
  # モデルのメタ情報
  class Meta:
    db_table = 'visitors'
    verbose_name = '来訪者'
    verbose_name_plural = '来訪者一覧'
    
  def __str__(self):
    return self.visitor_name