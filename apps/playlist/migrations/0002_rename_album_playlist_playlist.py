# Generated by Django 4.1.3 on 2022-12-23 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='album',
            new_name='playlist',
        ),
    ]
