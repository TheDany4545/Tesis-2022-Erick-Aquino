# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 21:13:43 2022

@author: eaqui
"""

import pandas as pd
import serial
import random
import matplotlib.pyplot as plt
import numpy as np
#import csv
#from itertools import count
#from matplotlib.animation import FuncAnimation
#import multiprocessing
#import time

import scipy.signal
import funcion_BPK_mt as fn
import pyhrv
import pyhrv.nonlinear as nl
import pyhrv.tools as tools
import biosppy
import nolds
import spectrum

#import sklearn as sk
#from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
#from sklearn.metrics import accuracy_score
#import random
from joblib import dump, load
import threading

def ejecutar_doc1():
    exec(open(r"Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Varilla Programadora\Códigos_microcontroladores\Python_Varilla\Varilla_programadora.py").read())
def ejecutar_doc2():
    exec(open(r"Z:\Universidad UVG\Sexto Año\Segundo Ciclo\Tesis\Tesis-2022-Erick-Aquino\Varilla Programadora\Códigos_modo_automático\Multiprocessing\Multiprocessing.py").read())

hilo1 = threading.Thread(target=ejecutar_doc1)
hilo2 = threading.Thread(target=ejecutar_doc2)
hilo1.start()
hilo2.start()