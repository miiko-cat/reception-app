import csv
from datetime import datetime

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from visitors.reception_forms import VisitorForm
from visitors.models import Visitor


# ── 受付画面 ───────────────────────────────────────────
def home(request):
    if request.method == "POST":
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save()
            return redirect("thanks", visitor_id=visitor.id)
    else:
        form = VisitorForm()
    return render(request, "visitors/home.html", {"form": form})


def thanks(request, visitor_id):
    visitor = get_object_or_404(Visitor, id=visitor_id, is_deleted=False)
    return render(request, "visitors/thanks.html", {"visitor": visitor})


# ── スタッフ判定 ────────────────────────────────────────
def is_reception_staff(user):
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name='reception').exists()
    )


# ── ヘルパー ────────────────────────────────────────────
def _valid_date(val):
    try:
        datetime.strptime(val, '%Y-%m-%d')
        return val
    except (ValueError, TypeError):
        return ''


def _build_visitor_qs(request):
    """GETパラメータを元にフィルター済みQuerySetを返す共通処理"""
    # show_all = 1 のときだけ論理削除済みデータも含める
    show_all = request.GET.get('show_all') == '1'
    qs = Visitor.objects.all() if show_all else Visitor.objects.filter(is_deleted=False)
    active_filters = {}

    for param, lookup in {
        'visitor_name': 'visitor_name__icontains',
        'visit_purpose': 'visit_purpose__icontains',
        'phone_number': 'phone_number__icontains',
        'email': 'email__icontains',
    }.items():
        value = request.GET.get(param, '').strip()
        if value:
            qs = qs.filter(**{lookup: value})
            active_filters[param] = value

    date_from = _valid_date(request.GET.get('date_from', ''))
    date_to   = _valid_date(request.GET.get('date_to',   ''))
    if date_from:
        qs = qs.filter(checked_in_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(checked_in_at__date__lte=date_to)

    return qs, active_filters, date_from, date_to, show_all


SORT_MAP = {
    'visitor_name': 'visitor_name', '-visitor_name': '-visitor_name',
    'checked_in_at': 'checked_in_at', '-checked_in_at': '-checked_in_at',
}


# ── ビュー ──────────────────────────────────────────────
def staff_logout(request):
    logout(request)
    return redirect(settings.LOGIN_URL)


@login_required
@user_passes_test(is_reception_staff)
@ensure_csrf_cookie
def visitor_list(request):
    qs, active_filters, date_from, date_to, show_all = _build_visitor_qs(request)

    sort = request.GET.get('sort', '-checked_in_at')
    visitors_qs = qs.order_by(SORT_MAP.get(sort, '-checked_in_at'))

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        rows_html = render_to_string(
            'visitors/staff/visitor_list_rows.html',
            {'visitors': visitors_qs},
            request=request,
        )
        return JsonResponse({'count': visitors_qs.count(), 'html': rows_html})

    return render(request, 'visitors/staff/visitor_list.html', {
        'visitors':       visitors_qs,
        'sort':           sort,
        'active_filters': active_filters,
        'date_from':      date_from,
        'date_to':        date_to,
        'show_all':       show_all,
        # トグルリンク用：今ONならOFFへ(=パラメータ削除)、今OFFなら'1'をセット
        'show_all_next':  None if show_all else '1',
        'sort_name_next': '-visitor_name' if sort == 'visitor_name' else 'visitor_name',
        'sort_date_next': 'checked_in_at' if sort == '-checked_in_at' else '-checked_in_at',
    })


@login_required
@user_passes_test(is_reception_staff)
def visitor_export_csv(request):
    """現在のフィルター条件でCSVダウンロード"""
    qs, _, _, _, _ = _build_visitor_qs(request)

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="visitors.csv"'

    writer = csv.writer(response)
    writer.writerow(['来訪者名', '来訪目的', '電話番号', 'メール', '受付日時', '状態'])
    for v in qs.order_by('-checked_in_at'):
        writer.writerow([
            v.visitor_name,
            v.visit_purpose,
            v.phone_number or '',
            v.email or '',
            v.checked_in_at.astimezone().strftime('%Y/%m/%d %H:%M'),
            '削除済み' if v.is_deleted else '有効'
        ])
    return response

def visitor_toggle_delete(request, visitor_id):
    """来訪者の論理削除フラグをON/OFFする(行内ボタンからのAJAX専用)"""
    visitor = get_object_or_404(Visitor, id=visitor_id)
    visitor.is_deleted = not visitor.is_deleted
    visitor.deleted_at = timezone.now() if visitor.is_deleted else None
    visitor.save(update_fields=['is_deleted', 'deleted_at'])
    return JsonResponse({'success': True, 'is_deleted': visitor.is_deleted})