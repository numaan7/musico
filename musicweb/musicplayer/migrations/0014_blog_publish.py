# Generated by Django 4.1.7 on 2023-04-02 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicplayer', '0013_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='publish',
            field=models.BooleanField(default=False),
        ),
    ]
