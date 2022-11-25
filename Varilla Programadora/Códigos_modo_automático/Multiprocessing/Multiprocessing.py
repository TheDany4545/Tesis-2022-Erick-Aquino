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
import funcion_BPK_mt as fn
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
            plt.pause(0.2)           
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
            plt.pause(0.2)
            ############################ better peak finder #############################

            # Function that looks the peaks on the derivative
            d_ecg, peaks_d_ecg = fn.decg_peaks(heart_data_filtered, data_list[n_list].time)
            plt.figure(3)
            plt.show()
            plt.pause(0.2)
            
            #Function with other parameters as height and x distance 0.65
            #Corrige los picos 0.59
            Rwave_peaks_d_ecg = fn.d_ecg_peaks(d_ecg,peaks_d_ecg,data_list[n_list].time,0.6,0.4)
            plt.figure(4)
            plt.show()
            plt.pause(0.2)
            
            #Grafica donde vemos la derivada y la original, pero comparando los picos de 
            #ambas graficas y poniendo el pico de la derivada en la original, esto para
            #descaratar falsos picos en la lectura del ECG
            Rwave_t = fn.Rwave_peaks(heart_data_filtered, d_ecg, Rwave_peaks_d_ecg,data_list[n_list].time)
           # plt.figure(5)
            plt.show()
            plt.pause(0.2)
            
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
            plt.pause(0.2)


            print('SD1 es:',SD1)
            print('SD2 es:',SD2)
            print('Centro es: ',centro)
             
            ############### Actualizar contadores ###########################
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
    


    





    
