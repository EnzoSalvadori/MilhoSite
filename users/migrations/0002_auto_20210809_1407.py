# Generated by Django 3.1 on 2021-08-09 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='espaco',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
