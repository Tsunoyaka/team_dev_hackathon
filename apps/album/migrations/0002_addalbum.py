# Generated by Django 4.1.3 on 2022-12-14 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('album', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddAlbum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_album', to='album.album')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_album', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
