# Generated by Django 3.1 on 2021-06-11 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210607_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='premium',
            field=models.CharField(default='0', max_length=5),
        ),
    ]