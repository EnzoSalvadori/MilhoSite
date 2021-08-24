import keras
import os
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
from milho.models import Imagem
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import matplotlib.pyplot as plt
import cv2
import numpy as np
import pandas
import tensorflow as tf
import psutil
import rasterio
from osgeo import gdal


SITE = "http://www.cornview.com/"

THRES_SCORE = 0.5
square_size = 500

def get_session():
	config = tf.compat.v1.ConfigProto()
	config.gpu_options.allow_growth = True
	return tf.compat.v1.Session(config=config)

local = os.getcwd()

CLASSES_FILE = local + '/retinaNET/classes.csv'
tf.compat.v1.keras.backend.set_session(get_session())

model_path = local + '/retinaNET/resnet152_csv_20_Final.h5'
print(model_path)

# load retinanet model
model = models.load_model(model_path, backbone_name='resnet152')
model = models.convert_model(model)

# load label to names mapping for visualization purposes
labels_to_names = pandas.read_csv(CLASSES_FILE,header=None).T.loc[0].to_dict()

def calculaHW(h,w):
	fh = True
	fw = True
	conth = 1
	contw = 1
	while fh == True:
		if(h/conth <= square_size):
			fh = False  
		else:
			conth += 1
	while fw == True:
		if(w/contw <= square_size):
			fw = False  
		else:
			contw += 1
	return(conth,contw)

def cropImagem(img,conth,contw,id_img,userEmail):
	boxes3 = []
	scores3 = []
	boxes4 = []
	scores4 = []
	Y = img.shape[0]
	X = img.shape[1]
	for i in range(0,conth):
		if ( square_size * (i+1) < Y):
			cropH1 = i*square_size
			cropH2 = (i+1)*square_size
		elif (conth == 1):
			cropH1 = 0
			cropH2 = Y
		else:
			ajusteH = (i+1)*square_size - Y
			cropH1 = i*square_size - ajusteH
			cropH2 = (i+1)*square_size - ajusteH

		for j in range(0,contw):
			if ( square_size * (j+1) < X):
				cropW1 = j*square_size
				cropW2 = (j+1)*square_size
			elif (contw == 1):
				cropW1 = 0
				cropW2 = X
			else:
				ajusteW = (j+1)*square_size - X
				cropW1 = j*square_size - ajusteW
				cropW2 = (j+1)*square_size - ajusteW

			crop_img = img[cropH1:cropH2, cropW1:cropW2]
			detect(crop_img,cropH1,cropW1,boxes3,scores3)

			if (cropH2+(square_size/2)) < Y:
				crop_img = img[int(cropH1+(square_size/2)):int(cropH2+(square_size/2)), cropW1:cropW2]
				detect(crop_img,int(cropH1+(square_size/2)),cropW1,boxes3,scores3)

			if (cropW2+(square_size/2)) < X:
				crop_img = img[cropH1:cropH2, int(cropW1+(square_size/2)):int(cropW2+(square_size/2))]
				detect(crop_img,cropH1,int(cropW1+(square_size/2)),boxes3,scores3)

			Imagem.objects.filter(id=id_img).update(porcentagemPro=(((i)*(contw)+(j+1))*100/(conth*contw)-1))	

	selected_indices = tf.image.non_max_suppression(
		boxes3, scores3, (len(boxes3)), iou_threshold=0.1
	)
	

	for i in selected_indices:
		largura = boxes3[i][2] - boxes3[i][0]
		altura = boxes3[i][3] - boxes3[i][1]
		if altura < 200 and largura < 200:
			boxes4.append(boxes3[i])
			scores4.append(scores3[i])

	desenha(img,boxes4,scores4,id_img,userEmail)    
				
def detect(image,H,W,boxes3,scores3):
	# preprocess image for network
	image = preprocess_image(image)
	image, scale = resize_image(image)
	# process image
	boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
	# correct for image scale
	boxes /= scale
	boxes2 = tf.squeeze(boxes)
	scores2 = tf.squeeze(scores)
	selected_indices = tf.image.non_max_suppression(
		boxes2, scores2, 300, iou_threshold=0.25
	)
	for i in selected_indices:
		boxes[0][i][0] = boxes[0][i][0] + W
		boxes[0][i][2] = boxes[0][i][2] + W
		boxes[0][i][1] = boxes[0][i][1] + H
		boxes[0][i][3] = boxes[0][i][3] + H
		boxes3.append(boxes[0][i])
		scores3.append(scores[0][i])

def desenha(image,boxes,scores,id_img,userEmail):
	draw = image.copy()
	cont = 0
	# visualize detections
	for i in range(len(boxes)):
	  # scores are sorted so we can break
		if scores[i] > THRES_SCORE:
			cont +=1
			meioX = int((boxes[i][2] - boxes[i][0])/2 + boxes[i][0])
			meioY = int((boxes[i][3] - boxes[i][1])/2 + boxes[i][1])
			cv2.circle(draw,(meioX,meioY), 3, (0,0,255), -1)
			#cv2.rectangle(draw,(int(boxes[i][0]),int(boxes[i][1])),(int(boxes[i][2]),int(boxes[i][3])),(0,0,255),2)
	#alterando os novos dados no banco 
	imagem = Imagem.objects.filter(id=id_img)
	cv2.imwrite("media/CV_"+str(imagem[0].imagemOrg), draw)
	tumb = cv2.resize(draw, (1280,720))
	cv2.imwrite("media/CV_"+str(imagem[0].imagemOrg)+".JPG", tumb)
	salva(cont,"CV_"+str(imagem[0].imagemOrg),id_img,userEmail,imagem,"CV_"+str(imagem[0].imagemOrg)+".JPG")

def salva(cont,draw,id_img,userEmail,imagem,tumb):
	imagem.update(imagemPro=draw,quantPlantas=cont,processada="2",porcentagemPro=100,tumbPro=tumb)
	if imagem[0].area == -1:
		ctx = {
		'user': userEmail.split("@")[0],
		'nome': str(imagem[0].imagemOrg) ,
		'plantas': str(imagem[0].quantPlantas),
		'imagemPro': SITE + "relatorio/"+str(imagem[0].id)
		}
		sendMail(userEmail,ctx,"reultado_email.html","Relatório")
	else:
		ctx = {
		'user': userEmail.split("@")[0],
		'nome': str(imagem[0].imagemOrg) ,
		'plantas': str(imagem[0].quantPlantas),
		'imagemPro': SITE + "relatorio/"+str(imagem[0].id),
		'area': str(round(imagem[0].area, 3)),
		'populacao': str(int(imagem[0].quantPlantas/imagem[0].area))
		}
		sendMail(userEmail,ctx,"reultado_email_2.html","Relatório")

# 0 inicial
# 1 em processamento
# 2 processada

def sendMail(email,ctx,html,sobre):
		subject, from_email, to = sobre, 'cornview@cornview.com', email
		text_content = ''
		html_content = render_to_string(html, ctx)
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

def processa(path_img,id_img,usuario):
	imagem = Imagem.objects.filter(id=id_img)
	imagem.update(processada = "1")
	#imagem foi para area de processamento
	if (psutil.virtual_memory()[2] >= 80): #se a menoria do servidor ja esta com se uso em 80% ou mais enviar a imagem para a fila 
		imagem.update(fila=True)
		return
	#se tudo estiver correto apenas processar a imagem
	try:
		img = cv2.imread(path_img)
		divh, divw = calculaHW(img.shape[0],img.shape[1])
		cropImagem(img,divh,divw,id_img,usuario.email)
	except Exception as e:
		print(e)
		if imagem[0].erro < 3:
			ctx = {
			'user': usuario.username,
			'imagem': imagem[0].imagemOrg
			}
			sendMail(usuario.email,ctx,"erro_email.html","Erro inesperado")#enviar um email para a conta da imagem avisando que um erro inesperado aconteceu 
			imagem.update(fila=True,processada=1,erro=imagem[0].erro+1) #imagem com erro no processamento vai para fila esperar para um novo processamento
		else:
			ctx = {
			'user': usuario.username,
			'imagem': imagem[0].imagemOrg
			}
			sendMail(usuario.email,ctx,"erro_email_2.html","Imagem invalida")#enviar um email para a conta da imagem avisando que um erro inesperado aconteceu 
			#excui as imagens da pasta media
			os.remove(imagem[0].imagemOrg.path)
			try:
				os.remove(imagem[0].imagemPro.path)
			except:
				pass
			try:
				os.remove(imagem[0].tumbPro.path)
			except:
				pass
			try:
				os.remove(imagem[0].tumb.path)
			except:
				pass
			#tirando o espaço da imagem do usuario
			usuario.espaco = usuario.espaco - imagem[0].tamanho
			usuario.save()
			#deletando a instancia do banco 
			imagem[0].delete()

def calArea(path_img):
	#verificando se a imagem esta no formato UTM correto para medir
	raster = rasterio.open(path_img)
	datum = raster.crs.wkt.split(" ")
	if "UTM" in datum:
		#se estiver no formato correto, calcular o tamanho da area de 1 pixel
		GDAL = gdal.Open(path_img)
		gt = GDAL.GetGeoTransform()
		pixelSizeX = gt[1]
		pixelSizeY =-gt[5]
		areaPix = pixelSizeX*pixelSizeY
		#encontrar os pixels de representação pelas cores
		r = raster.read(3)
		g = raster.read(2)
		b = raster.read(1)
		ndvi = np.empty(raster.shape, dtype=rasterio.float32)
		check = np.logical_or ( r > 0, g > 0 , b > 0)
		pixels = np.count_nonzero(check == True)
		#calcular a area total multiplicando a area de um pixel pela quantidade deles
		area = areaPix * pixels
		return area/10000 #dividir por 10000 para ter a area em Hectares
	else:
		return -1

#img = cv2.imread(path_img)
#divh, divw = calculaHW(img.shape[0],img.shape[1])
#cropImagem(img,divh,divw,id_img)

