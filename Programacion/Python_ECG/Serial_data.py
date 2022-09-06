# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 19:41:25 2022

@author: Daniel

"""

import serial
import csv
import pandas as pd

path= r'Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Programacion\Python_ECG\data.csv'
ser = serial.Serial(port=('COM7'),baudrate = 115200)
get_data = pd.read_csv(path,header = None) # lee csv
#get_data[0] = get_data[0].str.replace("'","") # Remove quotes 
#get_data[0] = get_data[0].str.replace(":"," ") #add space
#get_data[0] = get_data[0].str.replace("."," ",regex = False) #add space

################### Enviar linea por linea a traves del serial#################
d = len(get_data) #Cantidad de datos leido
i = 0
for i in range(10):
    line = get_data.loc[i,0]
    line2 = get_data.loc[i,1]
    send_line = line#.to_string(index = False)
    send_line2 = str(line2)
    ser.write(str.encode(send_line + send_line2 + "\n"))
    print(send_line + send_line2)
    

ser.close()