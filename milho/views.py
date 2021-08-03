from django.shortcuts import render,redirect
from django.http import JsonResponse
from allauth.account.decorators import verified_email_required
from django.contrib import messages
from milho.models import Imagem
import os
from .processa_imagem import processa
from threading import Thread
import cv2

LIMITE1 = 524288000 # 500MB
LIMITE2 = 53687063712 # 50 GB

def home(request):
	return render(request,"home.html")

def projetos(request):
	return render(request,"projetos.html")

def ajudeCont(request):
	return render(request,"ajude_cont.html")

@verified_email_required
def json(request):
	imagem = Imagem.objects.filter(processada = "1", fk_user = request.user)
	if len(imagem) == 0:
		return JsonResponse({'data' : '100'})
	if (imagem[0].fila == True):
		return JsonResponse({'data' : 'fila'})
	return JsonResponse({'data' : imagem[0].porcentagemPro})

@verified_email_required
def up(request):
	imagem = Imagem.objects.filter(processada = "1", fk_user = request.user)
	if request.method == 'POST':
		if len(imagem) > 0: #caso tente enviar outra imagem enquanto ja tem uma sendo processada
			return render(request,"up_img.html",{'imagem' : imagem})
		if 'imagem' in request.FILES:
			usuario = request.user
			uploaded_file = request.FILES['imagem']
			mbSize = uploaded_file.size/1048576
			mbSize = round(mbSize, 2)
			if (usuario.premium == "0"):
				if (usuario.espaco + uploaded_file.size <= (LIMITE1*2)) and (uploaded_file.size <= LIMITE1):
					usuario.espaco = usuario.espaco + uploaded_file.size
					cornImg = Imagem.objects.create_Imagem(uploaded_file,"default.jpg","0",usuario,mbSize)
					usuario.save()
					cornImg.save()
			if (usuario.premium == "1"):
				if (usuario.espaco + uploaded_file.size <= LIMITE2):
					usuario.espaco = usuario.espaco + uploaded_file.size
					cornImg = Imagem.objects.create_Imagem(uploaded_file,"default.jpg","0",usuario,mbSize)
					usuario.save()
					cornImg.save()
			oldName = cornImg.imagemOrg
			spl = str(oldName).split(".")
			local = os.getcwd()
			img = cv2.imread(local+"\\media\\"+str(oldName))
			if (spl[len(spl)-1].upper() == "TIFF" or spl[len(spl)-1].upper() == "TIF"):
				spl[len(spl)-1] = "JPG"
				tumbName = ".".join(spl)
				tumb = cv2.resize(img, (1280,720))
				cv2.imwrite(local+"\\media\\"+tumbName,tumb)
			else:
				tumbName = oldName
			Imagem.objects.filter(processada = "0", fk_user = request.user).update(altura=img.shape[0],largura=img.shape[1],tumb=tumbName) #adciona as infos de altura largura e uma tumbnail
	return render(request,"up_img.html",{'imagem' : imagem})

@verified_email_required
def imagens(request):
	if request.method == 'POST':
		id_img = request.POST.get("id")
		imagem = Imagem.objects.filter(id = id_img)
		if (imagem[0].processada == "2"):
			return redirect("pages:relatorio", id_img) 
	usuario = request.user
	imagens = Imagem.objects.filter(fk_user = usuario)
	return render(request, "imagens.html", {'imagens' : imagens})

@verified_email_required
def relatorio(request,id_img):
	imagem = Imagem.objects.filter(id = id_img)
	return render(request, 'processo.html',{'imagem' : imagem})

@verified_email_required
def processando(request):
	imagem = Imagem.objects.filter(processada = "0", fk_user = request.user)
	if len(imagem) > 0:
		path_img = imagem[0].imagemOrg.path 
		t1 = Thread(target=processa,args=[path_img,imagem[0].id,request.user.email])
		t1.start()
		return render(request, 'processando.html',{'imagem' : imagem})
	else:
		imagem = Imagem.objects.filter(processada = "1", fk_user = request.user)
	return render(request, 'processando.html',{'imagem' : imagem})

	