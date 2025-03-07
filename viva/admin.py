from django.contrib import admin
from .models import User, ShowInfo, Favorite

admin.site.register(User)
admin.site.register(ShowInfo)
admin.site.register(Favorite)
