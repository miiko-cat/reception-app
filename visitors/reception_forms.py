from django import forms
from django.forms import EmailInput, ModelForm, TextInput, Textarea

from visitors.models import Visitor

class VisitorForm(ModelForm):
  class Meta:
    model = Visitor
    fields = ['visitor_name', 'phone_number', 'email', 'visit_purpose']
    labels = {
      "visitor_name": "お名前",
      "phone_number": "電話番号",
      "email": "メールアドレス",
      "visit_purpose": "ご用件",
    }
    widgets = {
      "visitor_name": TextInput(attrs={"placeholder": "山田 太郎"}),
      "phone_number": TextInput(attrs={"placeholder": "090-1234-5678"}),
      "email": EmailInput(attrs={"placeholder": "example@example.com"}),
      'visit_purpose': Textarea(attrs={'rows': 5, "placeholder": "面談のご用件など"}),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # 必須フィールド
    self.fields["visitor_name"].required = True
    self.fields["visit_purpose"].required = True
    # 任意フィールド
    self.fields["phone_number"].required = False
    self.fields["email"].required = False