from django.contrib import admin
from django.urls import path
from visitors import views as visitors_views

urlpatterns = [
    path('', visitors_views.home, name='home'),
    path('thanks/<uuid:visitor_id>/', visitors_views.thanks, name='thanks'),    
    path('admin/', admin.site.urls),
]
