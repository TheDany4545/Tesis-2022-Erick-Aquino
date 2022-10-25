# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:01:33 2022

@author: Daniel
"""

import pandas as pd
import csv
import serial

#Lugar de destino para guardar los datos recibidos
path_save = r'C:\Users\Daniel\Desktop\dato_leido.csv' 
ser = serial.Serial(
        port= ('COM18'),
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
counter = 0
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
        if counter == 20:
            print('Se cerró la comunicación serial')
            break
    else:         
        print(decoded_line)
        with open(path_save,"a") as file:
            file.write(decoded_line + "\n")
        counter = 0
    #print(decoded_line)
    
ser.close()

