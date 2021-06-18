from django.urls import path

from .views import home
from .views import up
from .views import imagens
from .views import processo


app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("upload/", up, name="up"),
    path("imagens/", imagens, name="imagens"),
    path("processo/<int:id_img>", processo, name="proc"),
]