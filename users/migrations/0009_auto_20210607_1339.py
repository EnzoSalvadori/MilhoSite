# Generated by Django 3.1 on 2021-06-07 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_processada'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='processada',
            new_name='premium',
        ),
    ]
