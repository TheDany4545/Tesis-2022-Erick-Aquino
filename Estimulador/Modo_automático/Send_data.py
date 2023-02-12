import time
import serial
import pandas as pd



path = r'/home/pi/Desktop/Ejer1.csv'
#path = r'/home/pi/Desktop/Ejer1_prueba.csv'


ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

get_data = pd.read_csv(path,header = None) # lee csv
#get_data[0] = get_data[0].str.replace("'","") # Remove quotes 
#get_data[0] = get_data[0].str.replace(":"," ") #add space
#get_data[0] = get_data[0].str.replace("."," ") #add space

################### Enviar linea por linea a traves del serial#################
d = len(get_data) #Cantidad de datos leido
i = 0
for i in range(d):
    line = get_data.loc[i,0]
    line2 = get_data.loc[i,1]
    send_line = str(line)#.to_string(index = False)
    send_line2 = str(line2)
    ser.write(str.encode(send_line + "," + send_line2 + "\n")) #+ str.encode(send_line2))
    print(send_line + send_line2)
    '''
    line = get_data.loc[i]
    send_line = line.to_string(index = False)
    ser.write(str.encode(send_line))
    print(send_line)
    '''
    

#get_data.to_csv('DATOS_NUEVOS.csv', index = False)
ser.close()

'''
counter=0
temp = "Write counter: \n"

while 1:
        ser.write(temp.encode())
        time.sleep(1)
'''