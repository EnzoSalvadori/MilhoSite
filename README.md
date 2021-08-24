# WINDOWS

Python 3.7.7

https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/

pip install -r requeriments.txt

https://github.com/fizyr/keras-retinanet

cd keras-retinanet-master

python setup.py build_ext --inplace 

python setup.py install 

https://rasterio.readthedocs.io/en/latest/installation.html

python -m pip install GDAL-3.2.3-cp37-cp37m-win_amd64.whl

python -m pip install rasterio-1.2.3-cp37-cp37m-win_amd64.whl

NGINX (https://github.com/Johnnyboycurtis/webproject | https://www.youtube.com/watch?v=Dq9_U0bFffg&t=772s)

# UBUNTU

sudo add-apt-repository ppa:ubuntugis/ppa

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt-get update

sudo apt-get install python3.7

sudo apt-get install python3.7-dev

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 10

sudo apt-get install -y python3-opencv

sudo apt install python3-pip

sudo apt install git

https://docs.github.com/pt/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token

git clone https://github.com/EnzoSalvadori/MilhoSite.git

sudo python3 -m pip install -r requeriments.txt

sudo python3 -m pip install 

git clone https://github.com/EnzoSalvadori/keras-retinanet-install.git

sudo python3.7 setup.py build_ext --inplace 

sudo python3.7 setup.py install 

sudo python3 -m pip install opencv-python==4.5.2.52

sudo python3 -m pip uninstall numpy

sudo python3 -m pip install numpy==1.17.0

sudo python3 -m pip uninstall h5py

sudo python3 -m pip install h5py==2.10.0

sudo python3 -m pip install matplotlib==3.2.2

sudo python3 -m pip install pandas==1.0.5

sudo python3 -m pip install psutil==5.7.0

https://rasterio.readthedocs.io/en/latest/installation.html

sudo apt-get install gdal-bin libgdal-dev

sudo python3 -m pip install rasterio

cd usr/lib/python3/dist-packages/osgeo/

sudo mv _gdal.cpython-38-x86_64-linux-gnu.so _gdal.so
sudo mv _gdal_array.cpython-38-x86_64-linux-gnu.so _gdal_array.so
sudo mv _gdalconst.cpython-38-x86_64-linux-gnu.so _gdalconst.so  
sudo mv _gnm.cpython-38-x86_64-linux-gnu.so _gnm.so   
sudo mv _ogr.cpython-38-x86_64-linux-gnu.so _ogr.so  
sudo mv _osr.cpython-38-x86_64-linux-gnu.so _osr.so

sudo python3 -m pip install gdown

gdown https://drive.google.com/u/0/uc?id=10Sxho6ZJlOVymCD4l9QkgeMYc0S-pRC0&export=download (link drive do modelo) 

mv resnet152_csv_20.h5 resnet152_csv_20_Final.h5

sudo mkdir retinaNET

sudo mv resnet152_csv_20_Final.h5 retinaNET/

sudo nano classes.csv

Planta,0

sudo apt install nginx

cd etc/nginx/sites-enabled/

trocar as configurações default

sudo python3 manage.py collectstatic

sudo service nginx restart

sudo python3 manage.py migrate

apt-get install screen

pressionar as teclas CTRL+A+D. Essa combinação de teclas fará com que essa sessão virtual seja “separada”

screen (para iniciar qualquer comando antes)

screen -ls (para listar as sessões abertas)

screen -r (para restaurar a sessão)

screen -XS <session-id> quit

ps -ef (lista os processos que estão sendo executados)

sudo kill PID (mata o processo executado)

sudo python3 runserver.py

sudo python3 manage.py fila

# Ajustes

(lembrar de mudar o nome do site no banco de dados / ajustar link para nome do dominio do site verdadeiro no envio do email de relatorio)

