# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 19:41:25 2022

@author: Daniel

"""

import serial
import csv

path= r'Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Programacion\Python_ECG\data2.csv'
with open(path, "r") as my_file:
    # pass the file object to reader()
    file_reader = csv.reader(my_file)
    # do this for all the rows
    for i in file_reader:
        # print the rows
        print(i)