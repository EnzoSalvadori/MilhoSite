from django.shortcuts import render
from allauth.account.decorators import verified_email_required
from django.contrib import messages
from milho.models import Imagem

def home(request):
    return render(request,"home.html")

@verified_email_required
def up(request):
    if request.method == 'POST':
        if 'imagem' in request.FILES:
            uploaded_file = request.FILES['imagem']
            cornImg = pes = Imagem.objects.create_Imagem(uploaded_file,"",False,request.user)
            cornImg.save()
            messages.success(request, "Arquivo de imagem enviado!")
        else:
            messages.error(request, "Arquivo de imagem não selecioando!")
    return render(request,"up_img.html")
    