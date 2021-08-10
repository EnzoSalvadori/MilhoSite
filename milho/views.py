from django.shortcuts import render,redirect
from django.http import JsonResponse
from allauth.account.decorators import verified_email_required
from django.contrib import messages
from milho.models import Imagem
import os
from .processa_imagem import processa
from .processa_imagem import calArea
from threading import Thread
import cv2

LIMITE1 = 500 #MB 524288000 BYTES
LIMITE2 = 50000 #MB 53687063712 BYTES

def home(request):
	return render(request,"home.html")

def projetos(request):
	return render(request,"projetos.html")

def ajudeCont(request):
	return render(request,"ajude_cont.html")

@verified_email_required
def json(request):
	#envia as inofrmações para barra de porcentagem
	imagem = Imagem.objects.filter(processada = "1", fk_user = request.user)
	if len(imagem) == 0:
		#se estiver completo 100%
		return JsonResponse({'data' : '100'})
	if (imagem[0].fila == True):
		#se estiver ocupado manda a fila
		return JsonResponse({'data' : 'fila'})
		#se estiver tudo ok manda a porcentagem
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
			mbSize = uploaded_file.size/1048576 #dividindo para transformar BYTES em MB
			mbSize = round(mbSize, 2)
			if (usuario.premium == "0"):
				#verificando se o tamanho é compativel
				if (usuario.espaco + mbSize <= LIMITE1) and (mbSize <= LIMITE1):
					usuario.espaco = usuario.espaco + mbSize
					print(mbSize)
					cornImg = Imagem.objects.create_Imagem(uploaded_file,"default.jpg","0",usuario,mbSize)
					usuario.save()
					cornImg.save()
			if (usuario.premium == "1"):
				#verificando se o tamanho é compativel
				if (usuario.espaco + mbSize <= LIMITE2):
					usuario.espaco = usuario.espaco + mbSize
					cornImg = Imagem.objects.create_Imagem(uploaded_file,"default.jpg","0",usuario,mbSize)
					usuario.save()
					cornImg.save()
			oldName = cornImg.imagemOrg
			spl = str(oldName).split(".")
			local = os.getcwd()
			img = cv2.imread(local+"\\media\\"+str(oldName))
			#se a imagem é um TIF cirar a area da imagem e uma imagem JPG para usar de tumbnail
			if (spl[len(spl)-1].upper() == "TIFF" or spl[len(spl)-1].upper() == "TIF"):
				spl[len(spl)-1] = "JPG"
				tumbName = ".".join(spl)
				tumb = cv2.resize(img, (1280,720))
				cv2.imwrite(local+"\\media\\"+tumbName,tumb)
				area = calArea(cornImg.imagemOrg.path)
			else:
				tumbName = oldName
				area = -1
			Imagem.objects.filter(processada = "0", fk_user = request.user).update(altura=img.shape[0],largura=img.shape[1],tumb=tumbName,area=area) #adciona as infos de altura largura e uma tumbnail
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
	if request.method == 'POST':
		#verifica se a imagem que vai ser excluida pertence ao usuario
		if imagem[0].fk_user == request.user:
			#excui a imagem do banco e move para outra pasta
			try:
				#verificar se ja não existe uma imagem igual na lixeira
				os.rename(imagem[0].imagemOrg.path, "lixeira/" + str(imagem[0].imagemOrg))
			except:
				#se existir excluir ela em vez de copiar
				os.remove(imagem[0].imagemOrg.path)
			#sempre excluir a imagem processada
			os.remove(imagem[0].imagemPro.path)
			try:
				#verificar se exite uma tumbnail e excluir ela
				os.remove(imagem[0].tumb.path)
			except:
				pass
			#tirando o espaço da imagem do usuario
			usuario = request.user
			usuario.espaco = usuario.espaco - imagem[0].tamanho
			usuario.save()
			#deletando a instancia do banco 
			imagem[0].delete()
			imagens = Imagem.objects.filter(fk_user = usuario)
			return render(request, 'imagens.html',{'imagem' : imagem})
		#se não ele volta direto para a mesma pagina
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

	