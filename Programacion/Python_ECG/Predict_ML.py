import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import random


path = r'C:\Users\Daniel\Desktop\ECG\resultados_sin_d.csv'

rand = random.randint(1, 300)
print('El valor aleatorio es: ', rand )
resultados = pd.read_csv(path)
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
#input_data = (96.28405838,105.2147464,504.3684211) #ejercicio MIT 307 60 segs
#input_data = (28.112780899538947,60.21766990988758,315.0752688172043) #ejercicio MIT 322 60 segs
#input_data = (180.46866958812709,174.00529805152485,380.57142857142856) #ejercicio MIT 323 60 segs
input_data = (91.80776452505765,113.78252070624411,421.455882352941166) #ejercicio MIT 324 60 segs
#input_data = (8.05734513711931,12.616408608832602,395.6621621621622) #ejercicio MIT 325 60 segs


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
