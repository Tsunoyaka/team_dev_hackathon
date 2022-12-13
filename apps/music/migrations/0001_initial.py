# Generated by Django 4.1.3 on 2022-12-13 15:23

import apps.music.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=400, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='music_images')),
                ('time_length', models.DecimalField(blank=True, decimal_places=2, max_digits=20)),
                ('music', models.FileField(upload_to='musics', validators=[apps.music.utils.validate_is_audio])),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist', to=settings.AUTH_USER_MODEL)),
                ('genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='genres', to='music.genre')),
            ],
        ),
        migrations.CreateModel(
            name='LikeMusic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_likes', to='music.music')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='music_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]