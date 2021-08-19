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

sudo add-apt-repository ppa:deadsnakes/ppa

sudo apt-get update

sudo apt-get install python3.7

sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 10

sudo apt install python3-pip

sudo apt install git

https://docs.github.com/pt/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token

git clone https://github.com/EnzoSalvadori/MilhoSite.git

sudo apt-get install -y python3-opencv

sudo python3 -m pip install -r requeriments.txt

sudo apt-get install python3.7-dev

git clone https://github.com/EnzoSalvadori/keras-retinanet-install.git

sudo python3.7 setup.py build_ext --inplace 

sudo python3.7 setup.py install 

sudo python3 -m pip install matplotlib==3.2.2

sudo python3 -m pip install pandas==1.0.5

sudo python3 -m pip install psutil==5.7.0

https://rasterio.readthedocs.io/en/latest/installation.html

sudo apt-get install python-numpy gdal-bin libgdal-dev

sudo python3 -m pip install rasterio

sudo apt-get install libgdal-dev

export CPLUS_INCLUDE_PATH=/usr/include/gdal

export C_INCLUDE_PATH=/usr/include/gdal

sudo python3 -m pip install GDAL

cd usr/lib/python3/dist-packages/osgeo/

sudo mv _gdal.cpython-38-x86_64-linux-gnu.so _gdal.so
sudo mv _gdal_array.cpython-38-x86_64-linux-gnu.so _gdal_array.so
sudo mv _gdalconst.cpython-38-x86_64-linux-gnu.so _gdalconst.so  
sudo mv _gnm.cpython-38-x86_64-linux-gnu.so _gnm.so   
sudo mv _ogr.cpython-38-x86_64-linux-gnu.so _ogr.so  
sudo mv _osr.cpython-38-x86_64-linux-gnu.so _osr.so

sudo python3 -m pip install gdown

gdown link drive do modelo mv resnet152_csv_20.h5 /retinaNET/resnet152_csv_20_Final.h5

sudo mkdir retinaNET

sudo mv resnet152_csv_20.h5 retinaNET/

nano classes.csv

Planta,0

python3 manage.py runserver


# Ajustes

(lembrar de mudar o nome do site no banco de dados / ajustar link para nome do dominio do site verdadeiro no envio do email de relatorio)

