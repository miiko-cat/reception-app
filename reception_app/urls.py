from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from visitors import views as visitors_views

urlpatterns = [
    path('', visitors_views.home, name='home'),
    path('thanks/<uuid:visitor_id>/', visitors_views.thanks, name='thanks'),    
    path('admin/', admin.site.urls),
    
    # 受付担当用
    path('staff/login/', auth_views.LoginView.as_view(
        template_name='visitors/staff/login.html'
    ), name='staff_login'),
    path('staff/logout/', auth_views.LogoutView.as_view(), name='staff_logout'),
    path('staff/visitors/', visitors_views.visitor_list, name='staff_visitor_list'),
]
