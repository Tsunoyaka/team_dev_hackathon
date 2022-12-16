from django.contrib import admin

from .models import Music, Genre, LikeMusic

admin.site.register(Music)
admin.site.register(Genre)
admin.site.register(LikeMusic)
