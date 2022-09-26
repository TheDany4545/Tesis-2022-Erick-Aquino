import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import random
from sklearn.externals import joblib


path_MC = r'C:\Users\Daniel\Desktop\ECG\resultados_Nueva_data.csv'

rand = random.randint(1, 300)
print('El valor aleatorio es: ', rand )
resultados = pd.read_csv(path_MC)
results = resultados.drop(columns='Nombre',axis=1)
x = results.drop(columns='target',axis=1) #Me quedo con mis features
x = x.values
y = results['target'] # Me quedo con las salidas
y = y.values

x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                    test_size = 0.5,
                                                    stratify=y,
                                                    random_state= rand )
print(x.shape, x_train.shape, x_test.shape)

model = LogisticRegression()
model.fit(x_train, y_train)

#Precision en training data
x_train_prediction = model.predict(x_train)
training_data_accuracy = accuracy_score(x_train_prediction, y_train)
print('Accuracy of the Training data:', training_data_accuracy)

x_test_prediction = model.predict(x_test)
test_data_accuracy = accuracy_score(x_test_prediction, y_test)
print('Accuracy of the Test data:', test_data_accuracy)

################### INPUT #########################
#input_data = (13.58965485243332,26.504190375071182,404.5652173913044) # Resposo Data P31
#input_data = (24.64204884,28.66216291,254.7130435) #ejercicio bike 5 60 segs
#input_data = (28.112780899538947,60.21766990988758,315.0752688172043) #ejercicio MIT 322 60 segs
#input_data = (180.46866958812709,174.00529805152485,380.57142857142856) #ejercicio MIT 323 60 segs
#input_data = (8.05734513711931,12.616408608832602,295.6621621621622) #ejercicio MIT 325 60 segs
#input_data = (2.0264513569392224,1.4312474935367059,166.140350877193) #ejercicio NEW14
#input_data = (1.2322818340454906,1.3922182317935168,171.92727272727274) #ejercicio NEW15
input_data = (4.774133991825201,4.935848792840509,204.37777777777777) #ejercicio NEW16
#input_data = (8.142530319255803,10.335337440064551,355.4230769230769) #Resposo P10_1
#input_data = (9.630635074824735,16.05824359947251,365.92) #Resposo P10_2
#input_data = (10.002720718319964,19.43872283814529,421.72727272727275) #R#esposo P10_5

#cambiando un poco to numpy array
input_data_as_numpy_array = np.asarray(input_data)

#reshape the numpy array as we are predicting for only one instance
input_data_reshape = input_data_as_numpy_array.reshape(1,-1)

prediction = model.predict(input_data_reshape)
print(prediction)
if (prediction[0]==0):
  print('La persona esta en reposo según su ECG')
else:
  print('La persona esta haciedo un esfuerzo físico según su ECG')
  
#saving
filename = 'model.sav'
joblib.dump(clf,filename)
