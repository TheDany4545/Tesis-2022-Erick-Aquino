# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 08:16:25 2022

@author: Erick Daniel Aquino Paz
"""

################################# Librerias ##################################
import pandas as pd #CSV import ilbrary
import numpy as np 
import matplotlib.pyplot as plt
import scipy.signal
import funcion_BPK as fn

########################## Limipo variables ###########################
'''
for v in dir():
    exec('del '+ v)
    del v
'''
############################## Importing DATA ################################
column_names = ['time','ecg']
path= r'Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Programacion\Python_ECG\data.csv'

heart_data = pd.read_csv(path,names = column_names) # lee csv
#heart_data = heart_data.drop([0,1],axis =0) #Elimina encabezados default de Physiobank
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

############################# Filtro butterworth #############################

Wn = 0.2 #Cut out frequencies higher 50 hZ
b, a = scipy.signal.butter(4,Wn, 'low', analog = False) #filtro orden 4
heart_data_filtered = scipy.signal.filtfilt(b,a,heart_data.ecg)

################################# Graficas ##################################
plt.plot(heart_data.time, heart_data.ecg)
plt.plot(heart_data.time, heart_data_filtered)
#plt.show(()
############################# Posicion picos ################################

picos,_ = scipy.signal.find_peaks(heart_data_filtered,height=(0.4))
plt.plot(heart_data.time, heart_data_filtered)
plt.plot(heart_data.time[picos], heart_data_filtered[picos],"X")

############################ better peak finder #############################

# Function that looks the peaks on the derivative
d_ecg, peaks_d_ecg = fn.decg_peaks(heart_data_filtered, heart_data.time)
#Function with other parameters as height and x distance
#Corrige los picos
Rwave_peaks_d_ecg = fn.d_ecg_peaks(d_ecg,peaks_d_ecg,heart_data.time,0.59,0.3)
#Grafica donde vemos la derivada y la original, pero comparando los picos de 
#ambas graficas y poniendo el pico de la derivada en la original, esto para
#descaratar falsos picos en la lectura del ECG
Rwave_t = fn.Rwave_peaks(heart_data_filtered, d_ecg, Rwave_peaks_d_ecg,heart_data.time)

################################ RR interval ###############################
#comparamos un data point de un pico con el otro datapoint del siguiente pico
RR_intervalo = np.diff(Rwave_t)
#plt.figure()
#plt.plot(RR_intervalo)

######################### Caclcular el ritmo cardiaco #######################
#para hacer el calculo en pulsaciones por minuto se hace la conversión
heart_rate = (1/RR_intervalo)*60
plt.figure()
plt.plot(heart_rate)
plt.xlabel('Time [s]')
plt.ylabel('Pulsaciones')
plt.title('Pulsaciones por minuto')
##################### detectar el incremento de HR anormal ##################
dif_HR = np.diff(heart_rate)
plt.plot(dif_HR)
pos_dif_HR = abs(dif_HR)
####################### HEART RATE DIFFERENTIAL METHOD #######################

x = np.array(RR_intervalo)
x_sum = np.array(RR_intervalo)
num_interval = len(x)
n = 3
i=0
sumatoria =0

while i <= num_interval:
    sumatoria += i
    x_sum[i] = sumatoria
    i+= 1
print("EL VALOR ES " +str(sumatoria))
    



'''
def lorenz(x):
    scaled_prefix_sum = x.cumsum()/x.sum()
    return np.insert(scaled_prefix_sum, 0, 0)
lorenz_curve = lorenz(x)
plt.plot(np.linspace(0.0, 1.0, lorenz_curve.size), lorenz_curve)
'''

