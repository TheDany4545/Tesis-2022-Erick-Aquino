# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 20:13:06 2022

@author: Daniel
"""

############################## SE IMPORTAN LIBRERIAS ##########################
import pandas as pd
import csv
import serial
import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import multiprocessing
import numpy as np
import time

import scipy.signal
import funcion_BPK as fn
import pyhrv
import pyhrv.nonlinear as nl
import pyhrv.tools as tools
import biosppy
import nolds
import spectrum
################### GUARDAR LO QUE VIENE DEL SERIAL EN UN BUFFER###############
ser = serial.Serial(
        port= ('COM9'),
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

datos = []
data_list = [] #Aqui se guardan los df en distintos segundos
n_list = 0 #Que version de la lista estoy leyendo
val = 5

        
######################### Funcion formato de tiempo a Segundos###############
def to_seconds(hora):
    m, s, ms, = hora.split(" ")
    #return int(mins)*360 + int(segs) + float(ms)
    return int(m)*60 + int(s) + int(ms)/1000
def grafica():
    Wn = 0.2 #Cut out frequencies higher 50 hZ
    b, a = scipy.signal.butter(4,Wn, 'low', analog = False) #filtro orden 4
    heart_data_filtered = scipy.signal.filtfilt(b,a,df.ecg)
    return heart_data_filtered





while 1:
    try:
        if ser.inWaiting() != 0:
            read_line = ser.readline()
            decoded_line = read_line.decode('utf-8').rstrip()
            datos.append(decoded_line) #agrego datos a lo ultimo de la lista
            print (decoded_line)
            if ser.inWaiting() == 0:
                #global df
                df = pd.DataFrame(datos) 
                df = df[0].str.split(',', expand = True) #separa por comas
                df[0] = df[0].str.replace("'","") # Remove quotes 
                df[0] = df[0].str.replace(":"," ") # add space 
                df[0] = df[0].str.replace("."," ") # add space 
                df[0] = df[0].map(to_seconds)
                df.columns = ['time','ecg']
                df['ecg']=df['ecg'].astype(float)
                
                #df[['time','ecg']] = df[['time','ecg']].astype(int)
                

                print("Quiero ver cuantas veces te actualizas")
        if df[df.eq(val).any(1)].empty == False: #Si esta lleno, ejecutar funcion
            
            data_list.append(df)
            df = df.iloc[0:0] #vacio el dataframe
            datos.clear()
            val = val+5
            
            print ('****************** Si se encontro ************************')
            ##############################################################
            Wn = 0.2 #Cut out frequencies higher 50 hZ
            b, a = scipy.signal.butter(4,Wn, 'low', analog = False) #filtro orden 4
            heart_data_filtered = scipy.signal.filtfilt(b,a,data_list[n_list].ecg)
            n_list = n_list + 1
            ###############################################
            #grafica()
            #p1 = multiprocessing.Process(target=grafica)
            #p1.start()
            #p1.join()
            #p1 = multiprocessing.Process(target=grafica)
                

    except KeyboardInterrupt:
        ser.close()
    except NameError:
        continue
    


    





    
