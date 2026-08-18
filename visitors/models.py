import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

# 電話番号：半角数字とハイフンのみ許可
phone_number_validator = RegexValidator(
  regex=r'^[0-9\-]*$',
  message='電話番号は半角数字とハイフン（-）のみ入力できます。'
)

# メールアドレス：全角文字を禁止（半角の印字可能文字のみ許可）
email_halfwidth_validator = RegexValidator(
  regex=r'^[\x20-\x7E]*$',
  message='メールアドレスは半角文字のみ入力できます。'
)
 

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
  organization_name = models.CharField(
    max_length=255,
    null=True,
    blank=True,
    verbose_name='組織名'
  )
  visit_purpose = models.CharField(
    max_length=255,
    verbose_name='来訪目的'
  )
  phone_number = models.CharField(
    max_length=20,
    null=True,
    blank=True,
    verbose_name='電話番号',
    validators=[phone_number_validator]
  )
  email = models.CharField(
    max_length=255,
    null=True,
    blank=True,
    verbose_name='メールアドレス',
    validators=[email_halfwidth_validator]
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