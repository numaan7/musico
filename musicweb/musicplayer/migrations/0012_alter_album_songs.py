# Generated by Django 4.1.7 on 2023-04-02 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicplayer', '0011_remove_album_album_name_remove_album_artist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='songs',
            field=models.ManyToManyField(blank=True, to='musicplayer.song'),
        ),
    ]
