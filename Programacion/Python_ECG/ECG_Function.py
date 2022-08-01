# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 08:16:25 2022

@author: Daniel
"""

################################# Librerias ##################################
import pandas as pd #CSV import ilbrary
import numpy as np 
import matplotlib.pyplot as plt


############################## Importing DATA ################################
column_names = ['time','ecg']
path= r'Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Programacion\Python_ECG\data.csv'

heart_data = pd.read_csv(path,names = column_names) # lee csv
heart_data['time'] = heart_data['time'].str.replace("'","") # Remove quotes 
heart_data['time'] = heart_data['time'].str.replace(":"," ") #add space
heart_data['time'] = heart_data['time'].str.replace("."," ",regex = False) #add space

######################### Funcion formato de tiempo a Segundos###############
def to_seconds(hora):
    mins, segs, ms, = hora.split(" ")
    #return int(mins)*360 + int(segs) + float(ms)
    return int(segs)+float (ms)/1000

######################### Columna time en segundos###########################
heart_data['time'] = heart_data['time'].map(to_seconds)
print(heart_data)


plt.plot(heart_data.time, heart_data.ecg)
    
        

#ms to s
#heart_data = heart_data.t/1000
