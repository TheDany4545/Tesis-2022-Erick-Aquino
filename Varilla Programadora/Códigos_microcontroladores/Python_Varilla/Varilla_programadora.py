#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
SoftProg.py

Código que implementa el Software de Programación de la Fase II del Módulo de
Programación del Sistema VNS UVG

Basado en el código de TutoElectro: Tutorial_ESP8266_Python_1
Canal de youtube: https://www.youtube.com/c/Tutoelectro1/featured

Y también el código de Sentdex, lista de reproducción: GUIs with Tkinter (intermediate)
Canal de youtube: https://www.youtube.com/c/sentdex/featured

Miguel Alfonso Alvarez Sierra - 16168
Ingeniería Mecatrónica - UVG
"""


##############################################################################
# LIBRERIAS UTILIZADAS
##############################################################################
import socket # Librería socket para poder comunicarse con el ESP8266 por medio de WiFi
import select # Librería para monitorear sockets 

import serial # Librería para comunicación serial 
import serial.tools.list_ports # Módulo para poder ver los puertos seriales

import tkinter as tk # Librería para interfaz gráfica
from tkinter import ttk # Parte de la librería para mejorar el aspecto

import urllib # Librería para utilizar url
from urllib.request import urlopen # Parte de la librería para abrir un url

import time # Librería para poder utilizar delays 

##############################################################################
# DECLARACION DE VARIABLES
##############################################################################

# Tamaños de las fuentes a utilizar en la interfaz gráfica
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

# Variables para intento de conexión con la varilla programadora por WiFi
timeout = 3
retry = 2
delay = 2

comUSB = 0 # Confirmación de comunicación con USB

# Listas que incluyen las opciones programables de los parámetros de estimulación
#anchopts = ["250\u03BCs", "500\u03BCs", "25%", "50%", "75%"]
#freqopts = ["490.20 Hz", "30.64 Hz", "122.50 Hz", "245.10 Hz", 
#           "980.39 Hz", "3921.16 Hz", "31372.55 Hz", "Frecuencia 8"]
#opmodopts = ["Estimulacion", "Programacion", "Reposo"]
#timeopts = ["30 s", "60 s", "Tiempo 3", "Tiempo 4", "Tiempo 5"]
#sleepopts = ["5 min", "NO"]

anchopts = ["250 \u03BCs", "500 \u03BCs"]
freqopts = ["490.20 Hz", "30.64 Hz", "122.50 Hz", "245.10 Hz", 
           "980.39 Hz", "3921.16 Hz", "31372.55 Hz"]
opmodopts = ["0.25 mA", "0.5 mA", "0.75mA"]
timeopts = ["30 s", "60 s"]
sleepopts = ["5 min", "NO"]

##############################################################################
# CODIGO DE LA INTERFAZ GRAFICA
##############################################################################

class VNS(tk.Tk): # Clase principal de la interfaz gráfica, el core de la GUI
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs) 
        
        #tk.Tk.iconbitmap(self,"IconoUVG.ico") # Se coloca el icono de la UVG en la interfaz
        tk.Tk.wm_title(self,"Sistema VNS - UVG") # Se coloca el título a la interfaz
        
        # Se declara el contenedor para la GUI
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        
        # CODIGO PARA CREAR PESTAÑAS, UN MENUBAR        
        #menubar = tk.Menu(container)
        #filemenu = tk.Menu(menubar, tearoff=0)
        #filemenu.add_command(label="Save settings", command = lambda: popupmsg("Not supported"))
        #filemenu.add_separator()
        #menubar.add_cascade(label="File", menu=filemenu)
        
        #tk.Tk.config(self, menu=menubar)
        
        self.frames = {}
        
        # Se declaran los nombres de las páginas (ventanas) que se requieren
        for F in (StartPage, PageOne, PageTwo, PageThree):
    
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")
            
        
        self.show_frame(StartPage) # Se muestra la StartPage al iniciar
        
        
    def show_frame(self, cont): # Funcion para mostrar la página deseada 
        
        frame = self.frames[cont]
        frame.tkraise()
        

class StartPage(tk.Frame): # Página de inicio 
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        label = tk.Label(self, text="BIENVENIDO",font=LARGE_FONT) # Mensaje de bienvenida
        label.grid(row=0,column=3)
        
        # Se pide al usuario seleccionar la opción de conexión: wifi o usb
        label2 = tk.Label(self, text="Por favor seleccionar una opcion de conexion",font=NORM_FONT)
        label2.grid(row=1,column=3)
        
        def get_ports(): # Función para ver los puertos activos
            ports = serial.tools.list_ports.comports() # Ports guarda la lista de puertos
            # activos
            return ports

        foundPorts = get_ports() # Se obtienen los puertos disponibles
        
        def findArduino(portsFound): # Funcion para buscar la varilla programadora en los puertos
            commPort = 'None' # Condicion para errores
            numConnection = len(portsFound) # Numero de puertos activos 
    
            for i in range(0, numConnection): #Buscar en todos los puertos activos
                port = foundPorts[i] # Tomar el puerto que coincide con el contador
                strPort = str(port) # Convertir su nombre a string
        
                if 'Silicon' in strPort: # Se busca la palabra Arduino en el string
                    splitPort = strPort.split(' ') #Se separa el string en los espacios
                    commPort = (splitPort[0]) # Se guarda el puerto donde se encuentra 
                    # el Arduino
                    # Arduino aparece como COMX - Silicon Labs (COM7), lo que nos interesa
                    # es el COMX por eso tomamos el espacio 0 del string divido, lo que
                    # corresponde a COMX
    
            return commPort # Se retornoa el puerto del ESP8266
        
        def autoPorts(): # Función que contiene las dos anteriores para poder ser
            # utilizada al presionar un botón 
    
            foundPorts = get_ports()
            connectPort = findArduino(foundPorts) # Se busca el puerto del Arduino

            if(connectPort == 'None'):
                noSerial()
                    
            if connectPort != 'None': # Si se encontró el puerto
                comUSB = 1
                global ser
                ser = serial.Serial(connectPort, 115200) # Se conecta a éste
                succesfulSerial() 
                
        def isOpen(ip, port):
            s.settimeout(timeout)
            try:
                s.connect((ip, int(port)))
                return True
            except:
                return False

        def checkHost(ip, port):
            ipup = False
            for i in range(retry):
                if isOpen(ip, port):
                    ipup = True
                    break
                else:
                    time.sleep(delay)
            return ipup
        
        def connectTry():
            WiFiConnection = False
            if checkHost(ESP_IP, ESP_PORT):
                print(ESP_IP + " está activo")
                WiFiConnection = True
            else:
                print("Conexión fallida")
                print("Por favor conectar cable USB")
                WiFiConnection = False

            if(WiFiConnection == False):
                messageNoWiFi()
            else:
                succesfulWiFi()
     
        # Boton para intenter comunicacion por cable USB
        button2 = ttk.Button(self, text="Conectar por medio de cable USB",
                            command=autoPorts)
        button2.grid(row=3, column=3,sticky="ew") # Fila 1, columna 0
        
        # Boton para intentar comunicacion por WiFi
        button3 = ttk.Button(self, text="Conectar por medio de WiFi",
                            command=lambda: controller.show_frame(PageThree))
        button3.grid(row=2, column=3,sticky="ew") # Fila 1, columna 0
        
        
        def noSerial(): # Funcion para mostrar ventana de fallo de conexion por cable USB
            win = tk.Toplevel()
            win.title("CABLE USB NO CONECTADO") 
            
            def winDest(): # Funcion para cerrar la ventana y la app
                win.destroy()
                app.destroy()
            
            # Mensaje que aparece en la ventana
            message = "Por favor cerrar la aplicacion y conectar cable USB"
            label = tk.Label(win, text=message,font=SMALL_FONT)
            label.grid(row=2,column=2)
            
            # Boton para cerrar la aplicacion
            buttonTryAgain = ttk.Button(win, text="Cerrar aplicacion", command=winDest)
            buttonTryAgain.grid(row=3,column=2,sticky="ew")
        
        def succesfulWiFi(): # Funcion que muestra conexion exitosa por WiFi
            win = tk.Toplevel()
            win.title("CONEXION POR WIFI EXITOSA")
            
            message = "Se ha logrado la comunicación por WiFi"
            label = tk.Label(win, text=message,font=LARGE_FONT)
            label.grid(row=2,column=2)
            
            buttonWiFi = ttk.Button(win, text="Ir a la selección de parámetros",command=lambda: controller.show_frame(PageTwo))
            #buttonWiFi = ttk.Button(win, text="Ir a la selección de parámetros",command=lambda: controller.show_frame(PagePassword))
            buttonWiFi.grid(row=3,column=2,sticky="ew")
        
        def succesfulSerial(): # Funcion que muestra ventana de conexion exitosa por USB
            win = tk.Toplevel()
            win.title("CONEXION POR USB EXITOSA")
            
            message = "Se ha logrado la comunicacion por cable USB"
            label = tk.Label(win, text=message,font=NORM_FONT)
            label.grid(row=2,column=2)
            
            # Boton que lleva a la seleccion de parametros
            buttonWiFi = ttk.Button(win, text="Ir a la seleccion de parametros",command=lambda: controller.show_frame(PageOne))
            buttonWiFi.grid(row=3,column=2,sticky="ew")
            
        def messageNoWiFi():
            win = tk.Toplevel()
            win.title('ERROR: SIN WIFI')
    
            def popupWiFi():
                win.destroy()
        
            def destroyAll():
                win.destroy()
                app.destroy()
    
            message = "No se pudo conectar con ESP8266 por medio de WiFi." 
            message2 = "Conectar cable USB."
            label = tk.Label(win, text=message,font=NORM_FONT)
            label.grid(row=0,column=0)
            
            label2 = tk.Label(win, text=message2,font=NORM_FONT)
            label2.grid(row=1,column=0)
            buttonUSB = ttk.Button(win, text="Por favor, seleccionar la opción para conexión por cable USB",command=popupWiFi)
            buttonUSB.grid(row=2,column=0,sticky="ew")
            
            buttonSalir = ttk.Button(win, text="Salir de la aplicación", command=destroyAll)
            buttonSalir.grid(row=3,column=0,sticky="ew")
            
class PageOne(tk.Frame): #PAGINA PARA PARAMETROS POR SERIAL
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One",font=LARGE_FONT)
        
        
        def successParam(): # Funcion que muestra ventana de programacion exitosa
            win = tk.Toplevel()
            win.title("PARAMETROS RECIBIDOS")
            
            def winDestruccion():
                win.destroy()
            
            message = "Modulo de Estimulacion dice: Parametros Recibidos" 
            label = tk.Label(win, text=message,font=SMALL_FONT)
            label.grid(row=2,column=2)
            
            buttonSi = ttk.Button(win, text="Cerrar Ventana",command=winDestruccion)
            buttonSi.grid(row=3,column=2,sticky="ew")
            
        def noSuccessParam(): # Funcion que muestra ventana de programacion fallida
            win = tk.Toplevel()
            win.title("FALLO EN COMUNICACION RF")
            
            def winDestruccion():
                win.destroy()
            
            message = "Modulo de Estimulacion dice: Fallo en Recepcion de Parametros" 
            label = tk.Label(win, text=message,font=SMALL_FONT)
            label.grid(row=2,column=2)
            
            buttonNo = ttk.Button(win, text="Cerrar Ventana",command=winDestruccion)
            buttonNo.grid(row=3,column=2,sticky="ew")
                    
        def clear_all(): # Funcion para el boton que cierra el puerto y la ventana de
                    # la interfaz grafica
            ser.close() # Se cierra el puerto serial
            s.close() # Se cierra el socket
            app.destroy() # Se cierra la ventana de interfaz grafica
            
        def serialParSend(): # Funcion para el boton que envia los parametros seleccionados
            #en la interfaz a Arduino
          
            op1 = cl1.get() # Se obtiene el valor del primer dropdown
            if(op1 == opmodopts[0]): # Se almacena en variable la opcion correspondiente
                modo = 1
            elif(op1 == opmodopts[1]):
                modo = 2
            elif(op1 == opmodopts[2]):
                modo = 3
        
            op2 = cl2.get()
            if(op2 == anchopts[0]):
                ancho = 1
            elif(op2 == anchopts[1]):
                ancho = 2
            elif(op2 == anchopts[2]):
                ancho = 3
            elif(op2 == anchopts[3]):
                ancho = 4
            elif(op2 == anchopts[4]):
                ancho = 5
        
            op3 = cl3.get()
            if(op3 == timeopts[0]):
                time = 1
            elif(op3 == timeopts[1]):
                time = 2
            elif(op3 == timeopts[2]):
                time = 3
            elif(op3 == timeopts[3]):
                time = 4
            elif(op3 == timeopts[4]):
                time = 5
        
            op4 = cl4.get()
            if(op4 == freqopts[0]):
                freq = 1
            elif(op4 == freqopts[1]):
                freq = 2
            elif(op4 == freqopts[2]):
                freq = 3
            elif(op4 == freqopts[3]):
                freq = 4
            elif(op4 == freqopts[4]):
                freq = 5
            elif(op4 == freqopts[5]):
                freq = 6
            elif(op4 == freqopts[6]):
                freq = 7
            elif(op4 == freqopts[7]):
                freq = 8
        
            op5 = cl5.get()
            if(op5 == sleepopts[0]):
                sleep = 1
            elif(op5 == sleepopts[1]):
                sleep = 2
        
            condSend = True
            contSend = 0
            
            while(condSend == True): # Se envían los 5 parámetros
                if(contSend == 0):
                    ser.write(str(modo).encode()) # Se envia el valor a Arduino
                elif(contSend == 1):
                    ser.write(str(ancho).encode()) # Se envia el valor a Arduino
                elif(contSend == 2):
                    ser.write(str(time).encode()) # Se envia el valor a Arduino
                elif(contSend == 3):
                    ser.write(str(freq).encode()) # Se envia el valor a Arduino
                elif(contSend == 4):
                    ser.write(str(sleep).encode()) # Se envia el valor a Arduino
                
                elif(contSend == 5):
                    condSend = False
                    
                contSend += 1
    
            
            lec = ser.read() # Se lee el puerto serial 
            
            lecInt = int(lec) # Se convierte la lectura a entero 
            if(lecInt == 1): # Si la lectura es 1
                successParam() # Se logró la programación
            else: # Si no
                noSuccessParam() # No se logró la programación 

                    
        cl1 = tk.StringVar()
        cl1.set(opmodopts[0])

        cl2 = tk.StringVar()
        cl2.set(anchopts[0])

        cl3 = tk.StringVar()
        cl3.set(timeopts[0])

        cl4 = tk.StringVar()
        cl4.set(freqopts[0])

        cl5 = tk.StringVar()
        cl5.set(sleepopts[0])
        
        
        # DEFINICION DE BOTONES Y ENTRY BOX
        drop1 = tk.OptionMenu(self,cl1,*opmodopts)
        drop1.grid(row=1, column=1,sticky="ew")

        drop2 = tk.OptionMenu(self,cl2,*anchopts)
        drop2.grid(row=2, column=1,sticky="ew")

        drop3 = tk.OptionMenu(self,cl3,*timeopts)
        drop3.grid(row=3, column=1,sticky="ew")

        drop4 = tk.OptionMenu(self,cl4,*freqopts)
        drop4.grid(row=4, column=1,sticky="ew")

        drop5 = tk.OptionMenu(self,cl5,*sleepopts)
        drop5.grid(row=5, column=1,sticky="ew")

        label1 = tk.Label(self, text = "Corriente: ")
        label2 = tk.Label(self, text = "Ancho de pulso: ")
        label3 = tk.Label(self, text = "Tiempo: ")
        label4 = tk.Label(self, text = "Frecuencia: ")
        label5 = tk.Label(self, text = "Tiempo de sleep: ")

        label1.grid(column = 0, row = 1) # Fila 1, columna 0
        label2.grid(column = 0, row = 2) # Fila 2, columna 0
        label3.grid(column = 0, row = 3) # Fila 3, columna 0
        label4.grid(column = 0, row = 4) # Fila 4, columna 0
        label5.grid(column = 0, row = 5) # Fila 5, columna 0

        lbl_titulo = tk.Label(self, text="Seleccionar los parámetros de estimulación deseados", font=LARGE_FONT) # Texto del título=
        lbl_titulo.grid(row=0, column=0, columnspan=2, sticky="ew") # Se añade el título al contenedor

        btn_LEDOn = ttk.Button(self, text="ENVIAR", command=serialParSend) # Botón para envío
        btn_LEDOn.grid (row=8, column=0,columnspan=2,sticky="ew") # Ubicación del botón                                                    

        btn_Cierre = ttk.Button(self, text="CERRAR APP",command=clear_all) # Botón para cerrar la interfaz  
        btn_Cierre.grid (row=9, column=0,columnspan=2,sticky="ew") # Ubicación del botón
        

class PageTwo(tk.Frame): # PAGINA PARA PARAMETROS POR WIFI
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two",font=LARGE_FONT)
        
                
        def clear_all(): # Funcion para el boton que cierra el puerto y la ventana de
                    # la interfaz grafica
            s.close() # Se cierra el socket
            app.destroy() # Se cierra la ventana de interfaz grafica
        
        def wifiParSend(): # Función para enviar los parámetros por medio de WiFi
                    
            op1 = cl1.get() # Se obtiene el valor del primer dropdown
            if(op1 == opmodopts[0]): # Se almacena en variable la opción correspondiente
                modo = '1'
            elif(op1 == opmodopts[1]):
                modo = '2'
            elif(op1 == opmodopts[2]):
                modo = '3'
        
            op2 = cl2.get()
            if(op2 == anchopts[0]):
                ancho = '1'
            elif(op2 == anchopts[1]):
                ancho = '2'
            elif(op2 == anchopts[2]):
                ancho = '3'
            elif(op2 == anchopts[3]):
                ancho = '4'
            elif(op2 == anchopts[4]):
                ancho = '5'
        
            op3 = cl3.get()
            if(op3 == timeopts[0]):
                time = '1'
            elif(op3 == timeopts[1]):
                time = '2'
            elif(op3 == timeopts[2]):
                time = '3'
            elif(op3 == timeopts[3]):
                time = '4'
            elif(op3 == timeopts[4]):
                time = '5'
        
            op4 = cl4.get()
            if(op4 == freqopts[0]):
                freq = '1'
            elif(op4 == freqopts[1]):
                freq = '2'
            elif(op4 == freqopts[2]):
                freq = '3'
            elif(op4 == freqopts[3]):
                freq = '4'
            elif(op4 == freqopts[4]):
                freq = '5'
            elif(op4 == freqopts[5]):
                freq = '6'
            elif(op4 == freqopts[6]):
                freq = '7'
            elif(op4 == freqopts[7]):
                freq = '8'
        
            op5 = cl5.get()
            if(op5 == sleepopts[0]):
                sleep = '1'
            elif(op5 == sleepopts[1]):
                sleep = '2'
        
    
            # Se envían los parámetros por medio de WiFi al ESP8266
            s.send(modo.encode(encoding='utf_8'))  
            s.send(ancho.encode(encoding='utf_8'))  
            s.send(time.encode(encoding='utf_8'))
            s.send(freq.encode(encoding='utf_8'))  
            s.send(sleep.encode(encoding='utf_8'))
                        
            condRetWi = True # Condición para recibir confirmación del cliente
            
            while(condRetWi == True): # Mientras la condición sea True
                socket_list = [s] 
                
                rs, ws, es = select.select(socket_list,[],[],0) # El socket se quiere leer 
                
                for sock in rs: 
                    if sock == s: # Si el contador esta el socket 
                        dataIn = sock.recv(1024) # Se lee el socket, valor de 8 bits
                        condRetWi = False # Se sale del while
                        
            dataInt = int(dataIn)
            if(dataInt == 1):
                succesfulParam()
            else:
                unsuccesfulParam()
        
        
        def succesfulParam():
            win = tk.Toplevel()
            win.title("PARAMETROS RECIBIDOS")
            
            def winDestruccion():
                win.destroy()
                            
            message = "Modulo de Estimulacion dice: Parametros Recibidos" 
            label = tk.Label(win, text=message,font=SMALL_FONT)
            label.grid(row=2,column=2)
            
            buttonSi = ttk.Button(win, text="Cerrar Ventana",command=winDestruccion)
            buttonSi.grid(row=3,column=2,sticky="ew")
            
        def unsuccesfulParam(): 
            win = tk.Toplevel()
            win.title("FALLO EN COMUNICACION RF")
            
            def winDestruccion():
                win.destroy()
            
            message = "Modulo de Estimulacion dice: Fallo en recepcion de Parametros" 
            label = tk.Label(win, text=message,font=SMALL_FONT)
            label.grid(row=2,column=2)
            
            buttonNo = ttk.Button(win, text="Cerrar Ventana",command=winDestruccion)
            buttonNo.grid(row=3,column=2,sticky="ew")
            
                    
        cl1 = tk.StringVar()
        cl1.set(opmodopts[0])

        cl2 = tk.StringVar()
        cl2.set(anchopts[0])

        cl3 = tk.StringVar()
        cl3.set(timeopts[0])

        cl4 = tk.StringVar()
        cl4.set(freqopts[0])

        cl5 = tk.StringVar()
        cl5.set(sleepopts[0])
        
        
        # DEFINICION DE BOTONES Y ENTRY BOX
        drop1 = tk.OptionMenu(self,cl1,*opmodopts)
        drop1.grid(row=1, column=1,sticky="ew")

        drop2 = tk.OptionMenu(self,cl2,*anchopts)
        drop2.grid(row=2, column=1,sticky="ew")

        drop3 = tk.OptionMenu(self,cl3,*timeopts)
        drop3.grid(row=3, column=1,sticky="ew")

        drop4 = tk.OptionMenu(self,cl4,*freqopts)
        drop4.grid(row=4, column=1,sticky="ew")

        drop5 = tk.OptionMenu(self,cl5,*sleepopts)
        drop5.grid(row=5, column=1,sticky="ew")

        label1 = tk.Label(self, text = "Corriente: ")
        label2 = tk.Label(self, text = "Ancho de pulso: ")
        label3 = tk.Label(self, text = "Tiempo: ")
        label4 = tk.Label(self, text = "Frecuencia: ")
        label5 = tk.Label(self, text = "Tiempo de sleep: ")

        label1.grid(column = 0, row = 1) # Fila 1, columna 0
        label2.grid(column = 0, row = 2) # Fila 2, columna 0
        label3.grid(column = 0, row = 3) # Fila 3, columna 0
        label4.grid(column = 0, row = 4) # Fila 4, columna 0
        label5.grid(column = 0, row = 5) # Fila 5, columna 0

        lbl_titulo = tk.Label(self, text="Seleccionar los parámetros de estimulación deseados", font=LARGE_FONT) # Texto del título=
        lbl_titulo.grid(row=0, column=0, columnspan=2, sticky="ew") # Se añade el título al contenedor

        btn_LEDOn = ttk.Button(self, text="ENVIAR", command=wifiParSend) # Botón para envío
        btn_LEDOn.grid (row=8, column=0,columnspan=2,sticky="ew") # Ubicación del botón                                                    

        btn_Cierre = ttk.Button(self, text="CERRAR APP",command=clear_all) # Botón para cerrar la interfaz  
        btn_Cierre.grid (row=9, column=0,columnspan=2,sticky="ew") # Ubicación del botón
   
    
class PageThree(tk.Frame): # PAGINA PARA INGRESAR CODIGO IP DE LA VARILLA
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Three",font=LARGE_FONT)
        
    
        label = tk.Label(self, text="CODIGO",font=LARGE_FONT) # Mensaje de bienvenida
        label.grid(row=0,column=0)
        label2 = tk.Label(self, text="Ingrese el codigo de la Varilla Programadora",font=NORM_FONT)
        # Se pide al usuario seleccionar la opción de conexión: wifi o usb
        label2.grid(row=1,column=0)
        
        global ESP_IP

        global ESP_PORT
        ESP_PORT = 8266 # Puerto en el que se abrirá la comunicación

        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creación del objeto socket


        def isOpen(ip, port): #Funcion para ver si el puerto esta abierto 
            s.settimeout(timeout) # Timeout de 
            try:
                s.connect((ip, int(port)))
                return True
            except:
                return False

        def checkHost(ip, port):
            ipup = False
            for i in range(retry):
                if isOpen(ip, port):
                    ipup = True
                    break
                else:
                    time.sleep(delay)
            return ipup
        
        def connectTry():
            ESP_IP = e.get()
            WiFiConnection = False
            if checkHost(ESP_IP, ESP_PORT):
                WiFiConnection = True
            else:
                WiFiConnection = False

            if(WiFiConnection == False):
                messageNoWiFi()
            else:
                succesfulWiFi()
        
        def is_internet(): # Función para probar conexión a internet
            try: # Se intenta abrir el url (google es el más simple)
                urlopen('https://www.google.com', timeout = 1)
                return True # Si se pudo abrir se regresa True
            except urllib.error.URLError as Error:
                return False # Si no se pudo abrir se regresa False

        def try_internet(): # Función para indicar estado de la conexión a internet al usuario           
            if is_internet(): # Si se pudo abrir el url
                internetTry = 1
            else: # Si no
                internetTry = 0 
            return internetTry
        
        connectStatus = try_internet()
                
        if(connectStatus == 1):
            labelSi = tk.Label(self, text="Estado de Conexion a la Red: Conectado",fg="green",font=SMALL_FONT) # Mensaje de bienvenida
            labelSi.grid(row=4,column=0)
        else:
            labelNo = tk.Label(self, text="Estado de Conexion a la Red: No conectado",fg="red",font=SMALL_FONT) # Mensaje de bienvenida
            labelNo.grid(row=4,column=0)
             
        label4 = tk.Label(self, text=" Si el color es rojo, por favor seleccionar opcion para conectar por cable USB", font=SMALL_FONT)
        label4.grid(row=5,column=0)
        
        button = ttk.Button(self, text="Conectar por medio de WiFi",
                            command=connectTry)
        button.grid(row=3, column=0,sticky="ew") # Fila 1, columna 0
        
        buttonRet = ttk.Button(self, text="Regresar al Menu Principal",command=lambda: controller.show_frame(StartPage))
        buttonRet.grid(row=6,column=0,sticky="ew")
        
 
        def succesfulWiFi():
            win = tk.Toplevel()
            win.title("CONEXION POR WIFI EXITOSA")
            
            message = "Se ha logrado la comunicación por WiFi"
            label = tk.Label(win, text=message,font=LARGE_FONT)
            label.grid(row=2,column=2)
            
            buttonWiFi = ttk.Button(win, text="Ir a la selección de parámetros",command=lambda: controller.show_frame(PageTwo))
            buttonWiFi.grid(row=3,column=2,sticky="ew")
        
        def succesfulSerial():
            win = tk.Toplevel()
            win.title("CONEXION POR USB EXITOSA")
            
            message = "Se ha logrado la comunicación por cable USB"
            label = tk.Label(win, text=message,font=NORM_FONT)
            label.grid(row=2,column=2)
            
            buttonWiFi = ttk.Button(win, text="Ir a la selección de parámetros",command=lambda: controller.show_frame(PageOne))
            buttonWiFi.grid(row=3,column=2,sticky="ew")
            
        def messageNoWiFi():
            win = tk.Toplevel()
            win.title('ERROR: CODIGO INCORRECTO')
    
            def popupWiFi():
                
                win.destroy()
        
            def destroyAll():
                win.destroy()
                app.destroy()
    
            message = "No se pudo conectar con Varilla Programadora por medio de WiFi." 
            message2 = "Conectar cable USB."
            label = tk.Label(win, text=message,font=NORM_FONT)
            label.grid(row=0,column=0)
            
            label2 = tk.Label(win, text=message2,font=NORM_FONT)
            label2.grid(row=1,column=0)
            buttonUSB = ttk.Button(win, text="Regresar al Menu Principal",command=lambda: controller.show_frame(StartPage))
            buttonUSB.grid(row=2,column=0,sticky="ew")
            
            buttonAgain = ttk.Button(win, text="Intentar codigo de nuevo",command=popupWiFi)
            buttonAgain.grid(row=3,column=0,sticky="ew")
            
            buttonSalir = ttk.Button(win, text="Salir de la aplicacion", command=destroyAll)
            buttonSalir.grid(row=4,column=0,sticky="ew")
            
        e = tk.Entry(self, width=50)
        e.grid(row=2, column=0, sticky="ew")


      
app = VNS()
app.geometry("450x250")
app.mainloop()
        
        
        
    
    