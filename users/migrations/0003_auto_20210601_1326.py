# Generated by Django 3.1 on 2021-06-01 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210601_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='espaco',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='processada',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
