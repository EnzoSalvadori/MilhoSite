# Generated by Django 3.1 on 2021-08-13 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milho', '0004_imagem_tumbpro'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagem',
            name='erro',
            field=models.IntegerField(default=0),
        ),
    ]
