from django.db import models
from users.models import User

# Create your models here.

class ImagemManager(models.Manager):
    def create_Imagem(self,imagemOrg,imagemPro,processada,fk_user):
        imagem = self.create(imagemOrg=imagemOrg,imagemPro=imagemPro,processada=processada,fk_user=fk_user)
        return imagem

class Imagem(models.Model):
    class Meta:
        db_table = 'imagem'
    imagemOrg = models.ImageField(default="default.jpg")
    imagemPro = models.ImageField(default="default.jpg")
    quantPlantas = models.IntegerField(default=0)
    processada = models.CharField(max_length=5, default="0")
    fk_user = models.ForeignKey(User, on_delete=models.PROTECT)

    objects = ImagemManager()

    def __str__(self):
        return str(self.id)