# Generated by Django 4.1.7 on 2023-04-12 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicplayer', '0022_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(blank=True, to='musicplayer.tags'),
        ),
        migrations.AddField(
            model_name='song',
            name='tags',
            field=models.ManyToManyField(blank=True, to='musicplayer.tags'),
        ),
    ]
