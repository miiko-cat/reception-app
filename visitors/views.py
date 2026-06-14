from email import message
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from visitors.reception_forms import VisitorForm
from visitors.models import Visitor

# 受付画面
def home(request):
  # POSTリクエスト
  if request.method == "POST":
    form = VisitorForm(request.POST)
    if form.is_valid():
      visitor = form.save()
      # 登録完了画面にリクエスト
      return redirect("thanks", visitor_id=visitor.id)
    
  # GETリクエスト
  else:
    form = VisitorForm()
    
  return render(request, "visitors/home.html", {"form": form})

# 受付完了画面
def thanks(request, visitor_id):
  visitor = get_object_or_404(Visitor, id=visitor_id, is_deleted=False)
  return render(request, "visitors/thanks.html", {"visitor": visitor})

# 訪問者管理画面
def is_reception_staff(user):
  return user.is_authenticated and (
    user.is_superuser
    or user.groups.filter(name='reception').exists()
  )

@login_required
@user_passes_test(is_reception_staff)
def visitor_list(request):
  if not is_reception_staff(request.user):
    return HttpResponseForbidden(
      "このアカウントには来訪者一覧へのアクセス権限がありません。"
      "管理者に「reception」グループへの追加を依頼してください。"
    )
  qs = Visitor.objects.filter(is_deleted=False)
  
  # カラムごとのキーワード検索
  filters = {
    'visitor_name': 'visitor_name__icontains',
    'visit_purpose': 'visit_purpose__icontains',
    'phone_number': 'phone_number__icontains',
    'email': 'email__icontains',
  }
  active_filters = {}
  for param, lookup in filters.items():
    value = request.GET.get(param, '').strip()
    if value:
      qs = qs = qs.filter(**{lookup: value})
      active_filters[param] = value
      
  # 日付範囲
  date_from = request.GET.get('date_from', '')
  date_to = request.GET.get('date_to', '')
  if date_from:
    qs = qs.filter(checked_in_at__date__gte=date_from)
  if date_to:
    qs = qs.filter(checked_in_at__date__lte=date_to)
    
  SORT_FIELDS = {
      'visitor_name': 'visitor_name',
      '-visitor_name': '-visitor_name',
      'checked_in_at': 'checked_in_at',
      '-checked_in_at': '-checked_in_at',
  }
  sort = request.GET.get('sort', '-checked_in_at')
  order_by = SORT_FIELDS.get(sort, '-checked_in_at')
    
  return render(request, 'visitors/staff/visitor_list.html', {
    'visitors': qs.order_by(order_by),
    'sort': sort,
    'active_filters': active_filters,
    'date_from': date_from,
    'date_to': date_to,
    'sort_name_next': '-visitor_name' if sort == 'visitor_name' else 'visitor_name',
    'sort_date_next': 'checked_in_at'  if sort == '-checked_in_at' else '-checked_in_at',
  })