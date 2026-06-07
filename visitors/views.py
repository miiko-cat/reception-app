from email import message
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from visitors.reception_forms import VisitorForm
from visitors.models import Visitor

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


def thanks(request, visitor_id):
  visitor = get_object_or_404(Visitor, id=visitor_id, is_deleted=False)
  return render(request, "visitors/thanks.html", {"visitor": visitor})