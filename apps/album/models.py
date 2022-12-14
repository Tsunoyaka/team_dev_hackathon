from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from decouple import config

from apps.music.models import Music
from apps.music.utils import get_time
from slugify import slugify

User = get_user_model()


class Album(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='album'
    )
    album = models.CharField(max_length=200)
    image = models.ImageField(upload_to='album_images', default=config('DEFOULT_ALBUM_IMG'), blank=True)
    slug = models.SlugField(max_length=400, primary_key=True, blank=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.album + get_time())
        super().save(*args, **kwargs)

class MusAlbum(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='album_music'
    )
    musics = models.ForeignKey(to=Music, related_name='album_music', on_delete=models.CASCADE)
    album = models.ForeignKey(to=Album, related_name='album_music', on_delete=models.CASCADE)


class LikeAlbum(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='album_likes'
    )
    like_album = models.ForeignKey(
        to=Album,
        on_delete=models.CASCADE,
        related_name='album_likes'
    )

    def __str__(self) -> str:
        return f'Liked by {self.user.username}'

class AddAlbum(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='my_album'
    )
    album = models.ForeignKey(
        to=Album,
        on_delete=models.CASCADE,
        related_name='my_album'
    )