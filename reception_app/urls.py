from django.contrib import admin
from django.urls import path
from visitors import views as visitors_views

urlpatterns = [
    path('', visitors_views.index, name='index'),
    path('admin/', admin.site.urls),
]
