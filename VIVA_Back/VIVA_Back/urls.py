"""
URL configuration for VIVA_Back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
from myapp.views import (register_user, login_user, reset_password, get_shows, get_show_detail,
                         get_featured_shows, search_show, check_favorite, add_favorite, remove_favorite,
                         get_user_favorites, update_show, delete_show, create_show, get_all_show_details)

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/register/', register_user, name='register'),
    path('api/login/', login_user, name='login'),
    path('api/reset_password/',reset_password, name='reset_password'),
    path('api/get_shows/', get_shows, name='get_shows'),
    path('api/show_detail/', get_show_detail, name='get_show_detail'),
    path('api/featured_shows/', get_featured_shows, name='get_featured_shows'),
    path('api/search_show/', search_show, name='search_show'),
    path('api/check_favorite/', check_favorite, name='check_favorite'),
    path('api/add_favorite/', add_favorite, name='add_favorite'),
    path('api/remove_favorite/', remove_favorite, name='remove_favorite'),
    path('api/get_user_favorites/', get_user_favorites, name='get_user_favorites'),
    path('api/update_show/', update_show, name='update_show'),
    path('api/delete_show/', delete_show, name='delete_show'),
    path('api/create_show/', create_show, name='create_show'),
    path('api/get_all_show_details/', get_all_show_details, name='get_all_show_details'),
    path('admin/', admin.site.urls),
]
