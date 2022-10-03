"""BBS_09_28 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from blog import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register),
    path('get_code/', views.get_code),
    path('login/', views.login),
    path('', views.index),
    path('put_img/', views.put_img),
    path('comment/', views.comment),
    path('backend/',views.backend),
    path('delete/', views.delete),
    path('add_article/', views.add_article),
    path('edit_article/', views.edit_article),
    path('check_username/', views.check_username),
    path('logout/', views.logout),
    path('update_head/', views.update_head),
    path('update_pwd/', views.update_pwd),
    path('up_and_down/', views.up_and_down),
    path('<str:name>/articles/<int:pk>.html', views.article_detail),
    re_path('^(?P<name>\w+)/(?P<type_name>tag|category|archive)/(?P<condition>\d+).html', views.site),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('<str:name>/', views.site)
]
