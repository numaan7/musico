# Generated by Django 4.1.7 on 2023-03-30 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicplayer', '0007_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='product_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
