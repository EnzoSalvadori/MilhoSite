from django.shortcuts import render,redirect
from allauth.account.decorators import verified_email_required
from django.contrib import messages
from milho.models import Imagem
import os
#from .processa_imagem import processa
from threading import Thread
import cv2

LIMITE1 = 524288000 # 500MB
LIMITE2 = 53687063712 # 50 GB

def home(request):
	return render(request,"home.html")

@verified_email_required
def up(request):
	if request.method == 'POST':
		if 'imagem' in request.FILES:
			usuario = request.user
			uploaded_file = request.FILES['imagem']
			if (usuario.premium == "0"):
				if (usuario.espaco + uploaded_file.size <= LIMITE1):
					usuario.espaco = usuario.espaco + uploaded_file.size
					cornImg = Imagem.objects.create_Imagem(uploaded_file,"default.jpg","0",usuario)
					usuario.save()
					cornImg.save()
			if (usuario.premium == "1"):
				if (usuario.espaco + uploaded_file.size <= LIMITE2):
					usuario.espaco = usuario.espaco + uploaded_file.size
					cornImg = Imagem.objects.create_Imagem(uploaded_file,"default.jpg","0",usuario)
					usuario.save()
					cornImg.save()
			oldName = cornImg.imagemOrg
			spl = str(oldName).split(".")
			if (spl[len(spl)-1].upper() == "TIFF" or spl[len(spl)-1].upper() == "TIF"):
				local = os.getcwd()
				conv = cv2.imread(local+"\\media\\"+str(oldName))
				spl[len(spl)-1] = "JPG"
				newName = ".".join(spl)
				cv2.imwrite(local+"\\media\\"+newName,conv)
				imagem = Imagem.objects.filter(imagemOrg = oldName)
				imagem.update(imagemOrg = newName)
				os.remove(local+"\\media\\"+str(oldName))
	return render(request,"up_img.html")

@verified_email_required
def imagens(request):
	if request.method == 'POST':
		id_img = request.POST.get("id")
		imagem = Imagem.objects.filter(id = id_img)
		if (imagem[0].processada == "0"):
			path_img = imagem[0].imagemOrg.path 
			#mudar o campo de processada para 1 em processamento
			t1 = Thread(target=processa,args=[path_img,imagem[0].id,imagem[0].fk_user])
			t1.start()
			imagem.update(processada = "1")
		else:
			return redirect("pages:proc", id_img) #quando a imagem ja estiver processada entrar na outra pagina
	usuario = request.user
	imagens = Imagem.objects.filter(fk_user = usuario)
	return render(request, "imagens.html", {'imagens' : imagens})

@verified_email_required
def processo(request,id_img):
	imagem = Imagem.objects.filter(id = id_img)
	return render(request, 'processo.html',{'imagem' : imagem})

	