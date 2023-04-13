# Generated by Django 4.1.7 on 2023-04-01 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('musicplayer', '0010_alter_order_product_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='album',
            name='album_name',
        ),
        migrations.RemoveField(
            model_name='album',
            name='artist',
        ),
        migrations.RemoveField(
            model_name='album',
            name='image',
        ),
        migrations.RemoveField(
            model_name='album',
            name='url',
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]