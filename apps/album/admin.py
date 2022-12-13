from django.contrib import admin

from .models import Album, LikeAlbum, MusAlbum

admin.site.register(MusAlbum)
admin.site.register(Album)
admin.site.register(LikeAlbum)
