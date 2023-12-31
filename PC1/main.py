import cv2
import pickle
import numpy as np
import time

class EspacioTime:
    def __init__(self, coords):
        self.coords = coords
        self.tiempo_inicio = 0 
        self.tiempo_acumulado = 0
        self.ocupado = False

espacios = []
with open('espacios.pkl', 'rb') as file:
    espacios = pickle.load(file)

video = cv2.VideoCapture('video.mp4')

espacios_time = []
for i in espacios:
    espacios_time.append(EspacioTime(i))
check = True
while check:
    check, img = video.read()
    if not check:
     break
    imgBN = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgTH = cv2.adaptiveThreshold(imgBN, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)

    imgMedian = cv2.medianBlur(imgTH, 7)
    kernel = np.ones((5,5), np.int8)
    imgDil = cv2.dilate(imgTH, kernel)
    count_persons = 0
    time_now = time.time()
    for ind,rect in enumerate(espacios_time):
        x, y, w, h = rect.coords
        espacio = imgDil[y:y+h, x:x+w]
        total_espacio = espacio.size
        count = cv2.countNonZero(espacio)
        
        #cv2.putText(img, str(count), (x,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)
        #cv2.putText(img, str(t), (x,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,0), 1)

        if count < 3850:#3900:
            if rect.ocupado:
                rect.tiempo_acumulado += time_now-rect.tiempo_inicio
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            rect.ocupado = False

        else:
            if not rect.ocupado:
                rect.tiempo_inicio = time_now
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            rect.ocupado = True
        if rect.ocupado:
            count_persons += 1
    cv2.putText(img, "Personas: "+str(count_persons), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    cv2.imshow('video', img)
    #cv2.imshow('video BW', imgBN)
    #cv2.imshow('video TH', imgTH)
    #cv2.imshow('video Median', imgMedian)
    #cv2.imshow('video Dilatada', imgDil)
    cv2.waitKey(10)

time_now = time.time()
for e in espacios_time:
    if e.ocupado:
        e.tiempo_acumulado += time_now - e.tiempo_inicio
    
for i,e in enumerate(espacios_time):
    print("Tiempo acumulado en segundos para el espacio {} es : ".format(i+1),e.tiempo_acumulado)
