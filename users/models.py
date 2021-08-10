from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    espaco = models.FloatField(blank=True,default=0)
    premium = models.CharField(max_length=5, default="0")

    def __str__(self):
        return str(self.id)