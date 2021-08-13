from django.core.management.base import BaseCommand
import psutil
from milho.models import Imagem
from users.models import User
from threading import Thread
from milho.processa_imagem import processa
import time

class Command(BaseCommand):
	help = 'Command Customizado Teste'

	def handle(self, *args, **options):
		while True:
			if (psutil.virtual_memory()[2] >= 80): #se a menoria do servidor ja esta com se uso em 80% esperar mais 1 minuto
				time.sleep(60)
			else:
				imagem = Imagem.objects.filter(processada = "1", fila = True) #se não procura quem esta na fila e começa a processar
				for i in range(len(imagem)):
					path_img = imagem[i].imagemOrg.path 
					usuario = User.objects.filter(id = imagem[i].fk_user.id)
					t1 = Thread(target=processa,args=[path_img,imagem[i].id,usuario[0]])
					t1.start()
					Imagem.objects.filter(processada = "1", fk_user = imagem[i].fk_user).update(fila = False)
					if (psutil.virtual_memory()[2] >= 80): #se a memoria do servidor chegar em 80% parar de enviar novos processos
						i = len(imagem)
				time.sleep(60)