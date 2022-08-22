# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 19:41:25 2022

@author: Daniel

"""

import serial
import csv
import pandas as pd

path= r'Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Programacion\Python_ECG\data2.csv'
ser = serial.Serial(port=('COM4'),baudrate = 115200)
get_data = pd.read_csv(path,header = None) # lee csv
get_data[0] = get_data[0].str.replace("'","") # Remove quotes 
get_data[0] = get_data[0].str.replace(":"," ") #add space
get_data[0] = get_data[0].str.replace("."," ",regex = False) #add space

################### Enviar linea por linea a traves del serial#################
d = len(get_data) #Cantidad de datos leido
i = 0
for i in range(d):
    line = get_data.loc[i]
    send_line = line.to_string(index = False)
    ser.write(str.encode(send_line))
    print(send_line)
    

get_data.to_csv('DATOS_NUEVOS.csv', index = False)
ser.close()