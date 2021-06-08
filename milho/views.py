from django.shortcuts import render
from allauth.account.decorators import verified_email_required
from django.contrib import messages
from milho.models import Imagem

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
			if (usuario.premium == False):
				if (usuario.espaco + uploaded_file.size <= LIMITE1):
					usuario.espaco = usuario.espaco + uploaded_file.size
					cornImg = pes = Imagem.objects.create_Imagem(uploaded_file,"",False,usuario)
					usuario.save()
					cornImg.save()
			if (usuario.premium == True):
				if (usuario.espaco + uploaded_file.size <= LIMITE2):
					usuario.espaco = usuario.espaco + uploaded_file.size
					cornImg = pes = Imagem.objects.create_Imagem(uploaded_file,"",False,usuario)
					usuario.save()
					cornImg.save()
	return render(request,"up_img.html")
	