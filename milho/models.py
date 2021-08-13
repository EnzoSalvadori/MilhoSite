from django.db import models
from users.models import User
from django.utils import timezone

# Create your models here.

class ImagemManager(models.Manager):
    def create_Imagem(self,imagemOrg,imagemPro,processada,fk_user,tamanho):
        imagem = self.create(imagemOrg=imagemOrg,imagemPro=imagemPro,processada=processada,fk_user=fk_user,tamanho=tamanho)
        return imagem

class Imagem(models.Model):
    class Meta:
        db_table = 'imagem'
    imagemOrg = models.ImageField(default="default.jpg")
    imagemPro = models.ImageField(default="default.jpg")
    tumb = models.ImageField(default="default.jpg")
    tumbPro = models.ImageField(default="default.jpg")
    porcentagemPro = models.IntegerField(default=0)
    quantPlantas = models.IntegerField(default=0)
    tamanho = models.FloatField(default=0)
    altura = models.IntegerField(default=0)
    largura = models.IntegerField(default=0)
    processada = models.CharField(max_length=1, default="0")
    fila = models.BooleanField(default=False)
    erro = models.IntegerField(default=0)
    temp = models.DateTimeField(default=timezone.now)
    area = models.FloatField(default=-1)
    fk_user = models.ForeignKey(User, on_delete=models.PROTECT)

    
    objects = ImagemManager()

    def __str__(self):
        return str(self.id)