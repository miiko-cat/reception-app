from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from visitors import views as visitors_views

urlpatterns = [
    # 受付画面
    path('', visitors_views.home, name='home'),
    path('thanks/<uuid:visitor_id>/', visitors_views.thanks, name='thanks'),    
    path('admin/', admin.site.urls),
    
    # 管理者用
    path('staff/login/', auth_views.LoginView.as_view(
        template_name='visitors/staff/login.html'
    ), name='staff_login'),
    path('staff/visitors/', visitors_views.visitor_list, name='staff_visitor_list'),
    path('staff/visitors/<uuid:visitor_id>/toggle-delete/', visitors_views.visitor_toggle_delete, name='staff_visitor_toggle_delete'),
    path('staff/logout/', visitors_views.staff_logout, name='staff_logout'),
    
    # CSVエクスポート
    path('staff/visitors/export/', visitors_views.visitor_export_csv, name='staff_visitor_export'),
]
