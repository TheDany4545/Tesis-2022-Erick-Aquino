
################################# Librerias ##################################
import pandas as pd #CSV import ilbrary
import matplotlib.pyplot as plt
import scipy.signal
import funcion_BPK as fn
import pyhrv
import pyhrv.nonlinear as nl
import pyhrv.tools as tools
import numpy as np
import biosppy
import nolds
import spectrum
########################## Codigo ###########################
############################## Importing DATA ################################
column_names = ['time','ecg']
path= r'Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Programacion\Python_ECG\data.csv'
#r'C:\Users\Daniel\Desktop\ECG_v2\ECG_12h.csv'
#r'Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Programacion\Python_ECG\data.csv'

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
plt.show()
############################ better peak finder #############################

# Function that looks the peaks on the derivative
d_ecg, peaks_d_ecg = fn.decg_peaks(heart_data_filtered, heart_data.time)
plt.show()

#Function with other parameters as height and x distance
#Corrige los picos
Rwave_peaks_d_ecg = fn.d_ecg_peaks(d_ecg,peaks_d_ecg,heart_data.time,0.59,0.3)
plt.show()

#Grafica donde vemos la derivada y la original, pero comparando los picos de 
#ambas graficas y poniendo el pico de la derivada en la original, esto para
#descaratar falsos picos en la lectura del ECG
Rwave_t = fn.Rwave_peaks(heart_data_filtered, d_ecg, Rwave_peaks_d_ecg,heart_data.time)
plt.show()
################################ RR interval ###############################
#comparamos un data point de un pico con el otro datapoint del siguiente pico
RR_intervalo = 1/2*np.diff(Rwave_t)



#Load Sample Data
#signal = np.loadtxt(r'C:\Users\Daniel\Desktop\SampleECG.txt')[:,-1]

#Usando biosppy para los R peaks
#t,_,rpeaks = biosppy.signals.ecg.ecg(signal)[:3]
#t, filtered_signal, rpeaks = biosppy.signals.ecg.ecg(signal)[:3]

#Poincare compute
#results = pyhrv.nonlinear.poincare(rpeaks=t[rpeaks])

#nni = tools.nn_intervals(t[rpeaks])

#poincare plot
#figure()
#result = nl.poincare(nni)#,ellipse=True,vectors=True, legend = True)
nni_results = nl.poincare(RR_intervalo, ellipse= True, vectors= True, legend= True)

# SD1 (T) REFLEJA LA VARIACIÓN DE LATIDO A LATIDO / Variabilidad latido a latido
SD1 = nni_results['sd1']
# SD2 (L) RELFLEJA LAS FLUCTUACIONES GENERALES / Variabilidad en el tiempo
SD2 = nni_results['sd2']

print('SD1 es:',SD1)
print('SD2 es:',SD2)





