# Generated by Django 3.1 on 2021-06-19 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210619_1235'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='espaco1',
            new_name='espaco',
        ),
    ]