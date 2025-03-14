from django.contrib import admin
from .models import User
from .models import Favorite
from .models import Show

admin.site.register(User)
admin.site.register(Favorite)
admin.site.register(Show)
