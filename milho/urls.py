from django.urls import path

from .views import home
from .views import up
from .views import imagens
from .views import relatorio
from .views import processando
from .views import json
from .views import projetos
from .views import ajudeCont

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("upload/", up, name="up"),
    path("imagens/", imagens, name="imagens"),
    path("processando/", processando, name="processando"),
    path("json/", json, name="json"),
    path("relatorio/<int:id_img>", relatorio, name="relatorio"),
    path("projetos/", projetos, name="projetos"),
    path("contato/", ajudeCont, name="ajudeCont"),
]