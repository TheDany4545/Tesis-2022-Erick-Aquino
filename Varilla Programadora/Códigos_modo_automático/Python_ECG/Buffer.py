# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 20:13:06 2022

@author: Daniel
"""

################### GUARDAR LO QUE VIENE DEL SERIAL EN UN BUFFER###############
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

datos = []
'''
while 1:
    read_line = ser.readline()
    decoded_line = read_line.decode('utf-8').rstrip()
    if decoded_line ==  "":
        None
    if decoded_line != "":
        datos.append(decoded_line)
        print (decoded_line)
        '''
        
######################### Funcion formato de tiempo a Segundos###############
def to_seconds(hora):
    m, s, ms, = hora.split(" ")
    #return int(mins)*360 + int(segs) + float(ms)
    return int(m)*60 + int(s) + int(ms)/1000


while 1:
    try:
        if ser.inWaiting() != 0:
            read_line = ser.readline()
            decoded_line = read_line.decode('utf-8').rstrip()
            datos.append(decoded_line) #agrego datos a lo ultimo de la lista
            print (decoded_line)
            if ser.inWaiting() == 0:
                df = pd.DataFrame(datos) 
                df = df[0].str.split(',', expand = True) #separa por comas
                df[0] = df[0].str.replace("'","") # Remove quotes 
                df[0] = df[0].str.replace(":"," ") # add space 
                df[0] = df[0].str.replace("."," ") # add space 
                df[0] = df[0].map(to_seconds)
                print("Quiero ver cuantas veces te actualizas carnal")
    except KeyboardInterrupt:
        ser.close()
        
    
            
    
    
    
        
    




'''
fig = plt.figure(figsize=(7,3))
ax = fig.add_subplot()

fig.show
x = []
i = 0
l = 200

ser.close()
ser.open()

for i in range(l):
    ser1 = ser.readline().decode('utf-8').rstrip()
    print(ser1)
    ser2 = int(ser1)
    x.append(ser2)
    ax.plot(x,color = 'b')
    fig.canvas.draw()
    ax.set_xlim(left=max(0, i-30), rigth = i+60)
    plt.pause(0.0001)
plt.show()
'''
'''
read_line = ser.readline()
decoded_line = read_line.decode('utf-8').rstrip()
if decoded_line ==  "":
    print('No hay datos de entrada: ' + str(counter))
    counter = counter +1
    if counter == 10:
        print('Se cerró la comunicación serial')
'''
    
    
