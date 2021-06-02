from django.urls import path

from .views import home
from .views import up

app_name = "pages"

urlpatterns = [
    path("", home, name="home"),
    path("upload/", up, name="up"),
]