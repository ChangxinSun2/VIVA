from django.urls import path
from .views import home, register, user_login, user_logout, favorites, add_favorite, password_reset_request

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('favorites/', favorites, name='favorites'),
    path('add_favorite/<int:show_id>/', add_favorite, name='add_favorite'),
    path('password_reset/', password_reset_request, name='password_reset'),
]
