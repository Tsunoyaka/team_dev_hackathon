from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model
from .utils import get_time, get_audio_length, validate_is_audio
from django.urls import reverse

User = get_user_model()

class Genre(models.Model):
    genre = models.CharField(max_length=200, primary_key=True)

    def __str__(self) -> str:
        return self.genre


class Music(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=400, primary_key=True, blank=True)
    artist = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='artist'
    )
    image = models.ImageField(upload_to='music_images')
    genre = models.ForeignKey(to=Genre, blank=True,null=True, on_delete=models.SET_NULL, related_name='genres')
    time_length = models.DecimalField(blank=True, max_digits=20, decimal_places=2)
    music = models.FileField(upload_to='musics', validators=[validate_is_audio])

    def save(self,*args, **kwargs):
        if not self.time_length:
            audio_length=get_audio_length(self.music)
            self.time_length =f'{audio_length:.2f}'
        if not self.slug:
            self.slug = slugify(self.title + get_time())
        super().save(*args, **kwargs)

    def get_adsolute_url(self):
        return reverse('music-detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return f"""
        artist:{self.artist} 
        music: {self.title}"""



class LikeMusic(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='music_likes'
    )
    like_album = models.ForeignKey(
        to=Music,
        on_delete=models.CASCADE,
        related_name='music_likes'
    )

    def __str__(self) -> str:
        return f'Liked by {self.user.username}'
