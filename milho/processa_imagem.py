import keras
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color
from milho.models import Imagem
from django.shortcuts import render
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time
import pandas
import tensorflow as tf
THRES_SCORE = 0.5

square_size = 500

def get_session():
	config = tf.compat.v1.ConfigProto()
	config.gpu_options.allow_growth = True
	return tf.compat.v1.Session(config=config)

local = os.getcwd()

CLASSES_FILE = local + '\\retinaNET\\classes.csv'
tf.compat.v1.keras.backend.set_session(get_session())

model_path = local + '\\retinaNET\\resnet152_csv_20_Final.h5'
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

def cropImagem(img,conth,contw,id_img):
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

			print(len(boxes3))

	selected_indices = tf.image.non_max_suppression(
		boxes3, scores3, (len(boxes3)), iou_threshold=0.1
	)
	
	cont = 0
	for i in selected_indices:
		cont += 1
		print(cont)
		boxes4.append(boxes3[i])
		scores4.append(scores3[i])

	desenha(img,boxes4,scores4,id_img)    
				
def detect(image,H,W,boxes3,scores3):
	# preprocess image for network
	image = preprocess_image(image)
	image, scale = resize_image(image)
	# process image
	start = time.time()
	boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
	print("processing time: ", time.time() - start)
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

def desenha(image,boxes,scores,id_img):
	draw = image.copy()
	cont = 0
	# visualize detections
	for i in range(len(boxes)):
	  # scores are sorted so we can break
		if scores[i] > THRES_SCORE:
			cont +=1
			cv2.rectangle(draw,(int(boxes[i][0]),int(boxes[i][1])),(int(boxes[i][2]),int(boxes[i][3])),(0,0,255),2)
	#alterando os novos dados no banco 
	cv2.imwrite("media\\processada"+str(id_img)+".JPG", draw)
	salva(cont,"processada"+str(id_img)+".JPG",id_img)

def salva(cont,draw,id_img):
	imagem = Imagem.objects.filter(id=id_img).update(imagemPro=draw,quantPlantas=cont,processada="2")

def processa(path_img,id_img,fk_user):
	try:
		img = cv2.imread(path_img)
		divh, divw = calculaHW(img.shape[0],img.shape[1])
		cropImagem(img,divh,divw,id_img)
	except Exception as e:
		print("Erro no processamento")
		print(e)
		Imagem.objects.filter(id=id_img).update(processada="0")
		#mudar valor do campo processada para de erro e enviar um email para a conta da imagem avisando que um erro inesperado aconteceu 
	

#img = cv2.imread(path_img)
#divh, divw = calculaHW(img.shape[0],img.shape[1])
#cropImagem(img,divh,divw,id_img)

