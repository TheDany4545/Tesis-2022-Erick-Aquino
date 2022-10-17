#include <ESP8266WiFi.h> // Librería para WiFi con ESP8266
#include <WiFiClient.h> // Librería para poder usar ESP8266 como cliente con protocolo TCP
#include <LiquidCrystal_I2C.h> // Librería para poder utilizar la LCD I2C
#include <Wire.h> // Librería que permite la comunicación con dispositivos I2C
#include <SPI.h> // Librería para comunicarse por SPI
#include <nRF24L01.h> // Librería específica del módulo RF
#include <RF24.h> // Librería para uso del módulo RF

/**************************** MODIFICAR CON LOS DATOS DE LA RED ***************************/
const char* ssid = "Galaxy_Note9";
const char* password = "hola12345"; //2PM7H7601455
/******************************************************************************************/

/*************************************** NO MODIFICAR *************************************/
char dato, dato2, dato3, dato4, dato5; // Variables tipo char en las que se almacenan las lecturas de los parámetros por WiFi
//int modo, ancho, tiempo, freq, sleep; // Variables tipo int para almacenar los parámetros a enviar por RF
int mssg = 0; // Variable tipo int en la que se va almacenando la lectura del puerto serial
int cond1, cond2, cond3, cond4, cond5 = 0; // Condiciones para cambio de parámetro en la comunicación serial
byte modop[1]; // MODIFICAR A CORRIENTE // Bytes para RF
byte anctime[2];
byte freqsleep[2];

int wifiFlag = 0; // Bandera que indica si el ESP8266 se pudo conectar a la red WiFi
int cont = 0; // Contador de parámetros para la comunicación por WiFi

RF24 radio(0, 2); // Se instancia el módulo RF. CE = D2, CSN = D4

const byte addresses[][6] = {"00001", "00002"}; // Direcciones de escritura y lectura. Pensar en ellos más como canales que "nombre" del dispositivo

uint8_t dataBus[6]; // Bus de parámetros
uint8_t dataConf[2]; // Bus de confirmación

LiquidCrystal_I2C lcd(0x27, 16, 2); // Se declara la pantalla LCD con dirección 0x27, 16 columnas y 2 filas

WiFiServer servidorTCP(8266); // Declaración del puerto en el que se encuentra el Servidor
WiFiClient clienteTCP; // Declaración del nombre del cliente TCP


void setup() {
  //-------------------------------------Serial------------------------------------------------
  Serial.begin(115200); // Se inicializa la comunicación serial a una tasa de 115200
  while (!Serial);     // Se espera a ésta se haya terminado de inicializar
  //----------------------------------- initialize LCD------------------------------------------
  lcd.init();     // Inicia LCD
  lcd.backlight();// Turn on LCD backlight
  lcd.home();     // Se inicia escribiendo en (0,0)
  lcd.clear();    // Se borra pantalla para que inicie limpia


  //----------------------------------Conexion Wifi------------------------------------------------
  WiFi.begin(ssid, password); // Se intenta conectar a la red WiFi establecida

  for (int k = 0; k < 20; k++) // Se intenta conectar a la red cada 200 ms, 20 veces
  { // La conexión a la red no es rápida, por lo que se debe dar varios intentos antes de declarar que la conexión no fue exitosa
    if (WiFi.status() != WL_CONNECTED) // Si no está conectado a WiFi
    {
      delay(500); // Volver a intentarlo cada 200 ms
    }
  }

  // Luego de los 20 intentos, se revisa si la conexión fue exitosa por última vez
  if (WiFi.status() != WL_CONNECTED) // Si no lo fue
  {
    wifiFlag = 0; // Bandera de WiFi apagada

    //Serial.println("No se pudo conectar a la red"); // Se indica en el monitor serial que no fue exitosa la conexión
    //Serial.println("Conectar cable USB a la computadora");

    lcd.print("Conex. WiFi:"); // Se muestra en la pantalla LCD que no se pudo conectar a la red
    lcd.setCursor(0, 1);
    lcd.print("No exitosa");
  }

  else // Si la conexión fue exitosa
  {
    wifiFlag = 1; // Bandera de WiFi encendida

    //Serial.print("Conectado, IP: "); // Se indica que la conexión fue exitosa
    Serial.println(WiFi.localIP()); // Se muestra la IP del NodeMcu
    //Serial.println("");


    // Se muestra estado de conexión en pantalla LCD
    lcd.print("Conex. WiFi:");
    lcd.setCursor(0, 1);
    lcd.print("Exitosa");
    // Después de 3 segundos
    delay(3000);
    lcd.clear();
    // Se muestra la IP de la varilla programadora
    lcd.print("IP: ");
    lcd.setCursor(0, 1);
    lcd.print(WiFi.localIP()); // Se muestra la IP en la pantalla LCD

    servidorTCP.begin(); // Se inicializa el servidor TCP
  }
  //-----------------------------------Modulo de RF------------------------------------------------
  radio.begin(); // Se inicializa el módulo RF
  radio.setAutoAck(1); // Se asegura que el auto ACK esté activo
  radio.setChannel(110); // Se declara el canal de uso, 2510 MHz
  radio.openWritingPipe(addresses[1]); // Dirección 1 para escribir
  radio.openReadingPipe(1, addresses[0]); // Dirección 0 para leer
  radio.setDataRate(RF24_250KBPS); // Tasa de datos de 250 kbs
  radio.setPALevel(RF24_PA_MIN); // PA power al mínimo, -18 dBm
}

void loop() {

  if(wifiFlag == 1) // Si la conexión a la red WiFi fue exitosa 
  {
    if(!clienteTCP.connected()) // Si el cliente no está conectado al servidor definido 
    {
      clienteTCP = servidorTCP.available(); // Se intenta conectar al servidor disponible
    }
    else // Si ya está conectado
    {
      if(clienteTCP.available()) // Mientras hayan datos disponibles por WiFi
      {
        if(cont == 0) // Si es el primer parámetro
        {
          dato = clienteTCP.read(); // Se almacena el parámetro en una variable
          modop[0] = dato; // Se almacena la variable en el array correspondiente
        }
        else if(cont == 1) // Segundo parámetro 
        {
          dato2 = clienteTCP.read(); 
          anctime[0] = dato2; 
        }
        else if(cont == 2) // Tercer parámetro
        {
          dato3 = clienteTCP.read(); 
          anctime[1] = dato3; 
        }
        else if(cont == 3) // Cuarto parámetro
        {
          dato4 = clienteTCP.read();
          freqsleep[0] = dato4; 
        }
        else if(cont == 4) // Quinto parámetro
        {
          dato5 = clienteTCP.read();
          freqsleep[1] = dato5; 
        }
        cont++; // Aumentar el contador luego de cada lectura
      }

      if(cont == 5) // Si ya se recibieron todos los parámetros 
      {
        cont = 0; // Se reinicia el contador

        if(modop[0] == '1') // Se convierte a entero el valor recibido para poder enviarlo por RF
        {
          dataBus[0] = int(1); 
        }
        else if(modop[0] == '2')
        {
          dataBus[0] = int(2); 
        }
        else if(modop[0] == '3')
        {
          dataBus[0] = int(3); 
        }

        /* ANCHO DE PULSO */
        if(anctime[0] == '1'){
          dataBus[1] = int(1);
        }
        else if(anctime[0] == '2'){
          dataBus[1] = int(2);
        }
        else if(anctime[0] == '3'){
          dataBus[1] = int(3);
        }
        else if(anctime[0] == '4'){
          dataBus[1] = int(4);
        }
        else if(anctime[0] == '5'){
          dataBus[1]  = int(5);
        }

        /* TIEMPO DE ESTIMULACION */
        if(anctime[1] == '1'){
          dataBus[2] = int(1);
        }
        else if(anctime[1] == '2'){
          dataBus[2] = int(2);
        }
        else if(anctime[1] == '3'){
          dataBus[2] = int(3);
        }
        else if(anctime[1] == '4'){
          dataBus[2] = int(4);
        }
        else if(anctime[1] == '5'){
          dataBus[2] = int(5);
        }

        /* FRECUENCIA DE ESTIMULACION */
        if(freqsleep[0] == '1'){
          dataBus[3] = int(1);
        }
        else if(freqsleep[0] == '2'){
          dataBus[3] = int(2);
        }
        else if(freqsleep[0] == '3'){
          dataBus[3] = int(3);
        }
        else if(freqsleep[0] == '4'){
          dataBus[3] = int(4);
        }
        else if(freqsleep[0] == '5'){
          dataBus[3] = int(5);
        }
        else if(freqsleep[0] == '6'){
          dataBus[3] = int(6);
        }
        else if(freqsleep[0] == '7'){
          dataBus[3] = int(7);
        }
        else if(freqsleep[0] == '8'){
          dataBus[3] = int(8);
        }

        /* TIEMPO DE SLEEP */
        if(freqsleep[1] == '1'){
          dataBus[4] = int(1);
        }
        else if(freqsleep[1] == '2'){
          dataBus[4] = int(2);
        }

        dataBus[5] = 1; // Bit que le indica al receptor que ya puede enviar la confirmación

        delay(5);
        unsigned long start_timer = micros(); 
        radio.stopListening(); // Módulo RF como transmisor
        radio.write(&dataBus, sizeof(dataBus)); // Se escribe el bit de datos con su respectivo tamaño
        delay(5);

        radio.startListening(); // Módulo RF como receptor
        while(!radio.available()); // Si hay datos disponibles en el pipe
        radio.read(&dataConf, sizeof(dataConf)); // Se leen los datos y se almacenan en la confirmación
        unsigned long end_timer = micros(); 
        //Serial.println(dataConf[0]); 
        Serial.print("Transmission Time (us): ");
        Serial.println(end_timer - start_timer); 

        if(dataConf[0] == 1) // Si la confirmación es 1
        {
          clienteTCP.write("1"); // Se escribe al software de programación que la confirmación fue recibida
          dataBus[5] = 0;
        }
        else
        {
          clienteTCP.write("0"); // Se escribe al software de programación que la confirmación no fue recibida
        }

      }
    }
  }
  else{ // Si la conexión por WiFi no fue exitosa
      // Se procede a recibir datos por comunicación serial
      // Cada vez que se recibe un nuevo mensaje, se coloca un nueva condición en 1 para poder leer los 5 enviados desde la computadora sin errores
    if(Serial.available() & cond1 == 0)
    { // Si hay datos en el puerto serial
      mssg = Serial.read(); // Se lee el mensaje en mssg
      modop[0] = mssg; // Se almacena en el array correspondiente
      cond1 = 1; // Se coloca la condición en 1
      //lcd.setCursor(0,1);
      //lcd.print("Sent 1");
    }
    if(Serial.available() & cond1 == 1 & cond2 == 0)
    {
      mssg = Serial.read();
      anctime[0] = mssg;
      cond2 = 1;
      //lcd.setCursor(0,1);
      //lcd.print("Sent 2");
    }
    if(Serial.available() & cond1 == 1 & cond2 == 1 & cond3 == 0)
    {
      mssg = Serial.read();
      anctime[1] = mssg;
      cond3 = 1;
    }
    if(Serial.available() & cond1 == 1 & cond2 == 1 & cond3 == 1 & cond4 == 0)
    {
      mssg = Serial.read();
      freqsleep[0] = mssg;
      cond4 = 1;
    }
    if(Serial.available() & cond1 == 1 & cond2 == 1 & cond3 == 1 & cond4 == 1 & cond5 == 0)
    {
      mssg = Serial.read();
      freqsleep[1] = mssg;
      cond5 = 1;
    }

    // Al tener todas las condiciones en 1, indica que todos los mensajes fueron recibidos y almacenados
    if(cond1 == 1 & cond2 == 1 & cond3 == 1 & cond4 == 1 & cond5 == 1)
    { 
      cond1 = 0; // Se colocan todas las condiciones en 0 para poder recibir mensajes nuevos
      cond2 = 0;
      cond3 = 0;
      cond4 = 0; 
      cond5 = 0;

      // Dependiendo de lo recibido, se decide que parámetro va a ser el que se envíe

      /* MODO DE OPERACION */
      if(modop[0] == '1')
      {
        dataBus[0] = int(1);
      }
      else if(modop[0] == '2')
      {
        dataBus[0] = int(2);
      }
      else if(modop[0] == '3')
      {
        dataBus[0] = int(3);
      }

      /* ANCHO DE PULSO */
      if(anctime[0] == '1')
      {
        dataBus[1] = int(1);
      }
      else if(anctime[0] == '2')
      {
        dataBus[1] = int(2);
      }
      else if(anctime[0] == '3')
      {
        dataBus[1] = int(3);
      }
      else if(anctime[0] == '4')
      {
        dataBus[1] = int(4);
      }
      else if(anctime[0] == '5')
      {
        dataBus[1] = int(5);
      }

      /* TIEMPO DE ESTIMULACION*/
      if(anctime[1] == '1')
      {
        dataBus[2] = int(1);
      }
      else if(anctime[1] == '2')
      {
        dataBus[2] = int(2);
      }
      else if(anctime[1] == '3')
      {
        dataBus[2] = int(3);
      }
      else if(anctime[1] == '4')
      {
        dataBus[2] = int(4);
      }
      else if(anctime[1] == '5')
      {
        dataBus[2] = int(5);
      }

      /* FRECUENCIA DE ESTIMULACION */
      if(freqsleep[0] == '1')
      {
        dataBus[3] = int(1);
      }
      else if(freqsleep[0] == '2')
      {
        dataBus[3] = int(2);
      }
      else if(freqsleep[0] == '3')
      {
        dataBus[3] = int(3);
      }
      else if(freqsleep[0] == '4')
      {
        dataBus[3] = int(4);
      }
      else if(freqsleep[0] == '5')
      {
        dataBus[3] = int(5);
      }
      else if(freqsleep[0] == '6')
      {
        dataBus[3] = int(6);
      }
      else if(freqsleep[0] == '7')
      {
        dataBus[3] = int(7);
      }
      else if(freqsleep[0] == '8')
      {
        dataBus[3] = int(8);
      }

      /* TIEMPO DE SLEEP */
      if(freqsleep[1] == '1')
      {
        dataBus[4] = int(1);
      }
      else if(freqsleep[1] == '2')
      {
        dataBus[4] = int(2);
      }

      dataBus[5] = 1;

      delay(5);
      //unsigned long start_timer = micros(); 
      radio.stopListening();  
      radio.write(&dataBus, sizeof(dataBus)); 
      delay(5);

      radio.startListening(); 
      while(!radio.available()); 
      radio.read(&dataConf, sizeof(dataConf)); 

      if(dataConf[0] == 1)
      {
        Serial.print("1"); 
        dataBus[5] = 0;
      }
      else
      {
        Serial.print("0");
      } 
      
    }
  }
}
