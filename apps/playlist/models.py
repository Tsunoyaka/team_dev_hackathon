from django.db import models
from django.contrib.auth import get_user_model
from decouple import config

from apps.music.models import Music
from apps.music.utils import get_time
from slugify import slugify

User = get_user_model()


class Playlist(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='playlist'
    )
    playlist = models.CharField(max_length=200)
    image = models.ImageField(upload_to='playlist_images', default=config('DEFOULT_ALBUM_IMG'), blank=True)
    slug = models.SlugField(max_length=400, primary_key=True, blank=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.playlist + get_time())
        super().save(*args, **kwargs)


class MusPlaylist(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='playlist_music'
    )
    musics = models.ForeignKey(to=Music, related_name='playlist_music', on_delete=models.CASCADE)
    playlist = models.ForeignKey(to=Playlist, related_name='playlist_music', on_delete=models.CASCADE)

