from django.contrib import admin

from .models import Album, LikeAlbum, MusAlbum, AddAlbum

admin.site.register(MusAlbum)
admin.site.register(Album)
admin.site.register(LikeAlbum)
admin.site.register(AddAlbum)