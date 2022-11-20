# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 19:13:08 2022

@author: Daniel
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:01:33 2022

@author: Daniel
"""

import pandas as pd
import csv
import serial
import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#Lugar de destino para guardar los datos recibidos
path_save = r'C:\Users\Daniel\Desktop\dato_leido.csv' 
ser = serial.Serial(
        port= ('COM7'),
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
counter = 0
index = 0
#defino un funcion para poder leer lo que hay en el archivos csv
def animate(i):
    data_leida = pd.read_csv(path_save)
    eje_x = data_leida.iloc[:,0] #columna tiempo ms
    eje_y = data_leida.iloc[:,1] #columna voltaje mV
    
    plt.cla() # para que no cambia de colores al graficar
    plt.plot(eje_x, eje_y, label='Voltaje vs Tiempo')
    plt.legend(loc='upper left')
    #plt.tight_layout()


#Se borra lo que exista en el archivo
with open(path_save,'w') as f:
    pass
#Empiezo a leer los datos de la comunicacion serial, mientras no se envie nada
#hay un tiempo de espera, si no se envia nada durante esos segundos se cierra
#la comunicación serial 
#Si hay lectura de datos se guardan en un csv
while 1:
    read_line = ser.readline()
    decoded_line = read_line.decode('utf-8').rstrip()
    if decoded_line ==  "":
        print('No hay datos de entrada: ' + str(counter))
        counter = counter +1
        if counter == 10:
            print('Se cerró la comunicación serial')
            break
    else:         
        print(decoded_line)
        with open(path_save,"a") as file:
            file.write(decoded_line + "\n")
        counter = 0
        ani = FuncAnimation(plt.gcf(),  animate, interval=1000)
        index= index+1
        print(index)
        if index == 30:
            index = 0
            plt.pause(0.01)
        #plt.show()
        #plt.pause(0.01)
        
    #print(decoded_line)
    
ser.close()

