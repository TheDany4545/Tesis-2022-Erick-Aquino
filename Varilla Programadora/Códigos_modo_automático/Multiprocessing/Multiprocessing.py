# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 20:13:06 2022

@author: Daniel
"""

############################## SE IMPORTAN LIBRERIAS ##########################
import pandas as pd
import serial
import random
import matplotlib.pyplot as plt
import numpy as np
import csv
from itertools import count
from matplotlib.animation import FuncAnimation
import multiprocessing
import time

import scipy.signal
import funcion_BPK_mt as fn
import pyhrv
import pyhrv.nonlinear as nl
import pyhrv.tools as tools
import biosppy
import nolds
import spectrum

import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import random
from joblib import dump, load
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
save_predictions = []
n_list = 0 #Que version de la lista estoy leyendo
val = 5
val_stop = 19

        
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
            #######################Filto Butterworth #########################
            Wn = 0.2 #Cut out frequencies higher 50 hZ
            b, a = scipy.signal.butter(4,Wn, 'low', analog = False) #filtro orden 4
            heart_data_filtered = scipy.signal.filtfilt(b,a,data_list[n_list].ecg)

            ################################# Graficas ##################################
            plt.figure(1)
            plt.plot(data_list[n_list].time, data_list[n_list].ecg)
            plt.plot(data_list[n_list].time, heart_data_filtered)
            plt.xlabel('Segundos (S)')
            plt.ylabel('Milivoltios (mV)')
            
            plt.show()
            plt.pause(0.02)           
            ############################# Posicion picos ################################
            voltaje = 0.4
            picos,_ = scipy.signal.find_peaks(heart_data_filtered,height=(voltaje))
            plt.figure(2)
            plt.plot(data_list[n_list].time, heart_data_filtered)
            plt.plot(data_list[n_list].time[picos], heart_data_filtered[picos],"X")
            plt.axhline(voltaje, color = 'black', label = 'threshold')
            plt.xlabel('Segundos (S)')
            plt.ylabel('Milivoltios (mV)')
            
            plt.show()
            plt.pause(0.02)
            ############################ better peak finder #############################

            # Function that looks the peaks on the derivative
            d_ecg, peaks_d_ecg = fn.decg_peaks(heart_data_filtered, data_list[n_list].time)
            plt.figure(3)
            plt.show()
            plt.pause(0.02)
            
            #Function with other parameters as height and x distance 0.65
            #Corrige los picos 0.59
            Rwave_peaks_d_ecg = fn.d_ecg_peaks(d_ecg,peaks_d_ecg,data_list[n_list].time,0.6,0.4)
            plt.figure(4)
            plt.show()
            plt.pause(0.02)
            
            #Grafica donde vemos la derivada y la original, pero comparando los picos de 
            #ambas graficas y poniendo el pico de la derivada en la original, esto para
            #descaratar falsos picos en la lectura del ECG
            Rwave_t = fn.Rwave_peaks(heart_data_filtered, d_ecg, Rwave_peaks_d_ecg,data_list[n_list].time)
           # plt.figure(5)
            plt.show()
            plt.pause(0.02)
            
            ################################ RR interval ###############################
            #comparamos un data point de un pico con el otro datapoint del siguiente pico

            RR_intervalo = 1/2*np.diff(Rwave_t) #Despues de la derivada
            nni_results = nl.poincare(RR_intervalo, ellipse= True, vectors= True, legend= True)
            

            # SD1 (T) REFLEJA LA VARIACIÓN DE LATIDO A LATIDO / Variabilidad latido a latido
            SD1 = nni_results['sd1']
            # SD2 (L) RELFLEJA LAS FLUCTUACIONES GENERALES / Variabilidad en el tiempo
            SD2 = nni_results['sd2']
            centro = nni_results['centro']
            #plt.figure(6)
            #plt.show()
            plt.pause(0.02)


            print('SD1 es:',SD1)
            print('SD2 es:',SD2)
            print('Centro es: ',centro)
            
            ################################ MODELO ENTRENADO #############################
            model = load(r'Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Varilla Programadora\Códigos_modo_automático\Python_ECG\Modelo_entrenado.joblib')
            input_data = (SD1,SD2,centro) #ejercicio NEW16
            #input_data = (8.142530319255803,10.335337440064551,355.4230769230769) #Resposo P10_1
            #input_data = (9.630635074824735,16.05824359947251,365.92) #Resposo P10_2
            #input_data = (10.002720718319964,19.43872283814529,421.72727272727275) #R#esposo P10_5

            #cambiando un poco to numpy array
            input_data_as_numpy_array = np.asarray(input_data)

            #reshape the numpy array as we are predicting for only one instance
            input_data_reshape = input_data_as_numpy_array.reshape(1,-1)

            prediction = model.predict(input_data_reshape)
            save_predictions.append(prediction[0])
            print(prediction)
            if (prediction[0]==0):
              print('La persona esta en reposo según su ECG')
            else:
              print('La persona esta haciedo un esfuerzo físico según su ECG')
             
            ############### Actualizar contadores ###########################
            n_list = n_list + 1
            ###############################################
            #grafica()
            #p1 = multiprocessing.Process(target=grafica)
            #p1.start()
            #p1.join()
            #p1 = multiprocessing.Process(target=grafica)
        if df[df.eq(val_stop).any(1)].empty == False: #Si esta lleno, ejecutar funcion
            ser.close()
            break
        
    except KeyboardInterrupt:
        ser.close()
    except NameError:
        continue
print ('El resumen de predicciones de cada 20 segs es:',save_predictions)

guardar_datos = input('¿Quieres guardar los datos para un análisis posterior? Y/N ')

if guardar_datos == "Y":
    print("Se han guardado los valores")
elif guardar_datos == "N":
    print("No se han guardado los valores")
else:
    print("No es un caracter válido")
    

    





    
