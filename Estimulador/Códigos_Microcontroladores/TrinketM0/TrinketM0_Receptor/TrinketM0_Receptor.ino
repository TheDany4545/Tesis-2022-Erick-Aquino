/* StimModProg.ino
 * 
 * Código que implementa el módulo de recepción (simulación del módulo de estimulación) del
 * Módulo de Programación del Sistema VNS UVG
 * 
 * Basado en el código de Aqib: nRF24L01 Interfacing with Arduino | Wireless Communication
 * Link: https://create.arduino.cc/projecthub/muhammad-aqib/nrf24l01-interfacing-with-arduino-wireless-communication-0c13d4
 * 
 * Miguel Alfonso Alvarez Sierra - 16168 
 * Ingeniería Mecatrónica - UVG
 */

#include <SPI.h> // Librería para comunicarse con SPI
#include <nRF24L01.h> // Librería específica del módulo RF
#include <RF24.h> // Librería para uso del módulo RF

//RF24 radio(9, 10); // Instancia del módulo RF. CE = pin 9, CSN = pin 10 ARDUINO
RF24 radio(1, 0); // CE= D1, CSN= D0 //Trinket Receptor, ESP8266 Emisor

const byte addresses [][6] = {"00001", "00002"}; // Direcciones de escritura y lectura 

int contSec = 0;

uint8_t dataBus[6]; // Bus de parámetros

uint8_t dataConfOut[2]; // Bus de confirmación
uint8_t dataControl = 0; // Variable para salir del modo de lectura

void setup()
{
  Serial.begin(115200); // Se inicializa la comunicación serial a una tasa de 115200

  radio.begin(); // Se inicializa el módulo RF
  radio.setChannel(110); // Canal 100, 2510 MHz
  radio.openWritingPipe(addresses[0]); // Dirección 0 para escribir
  radio.openReadingPipe(1, addresses[1]); // Dirección 1 para leer
  radio.setDataRate(RF24_250KBPS); // Tasa de datos de 250 kbps
  radio.setPALevel(RF24_PA_MIN); // PA power al mínimo, -18 dBm

}

void loop()
{
  delay(5); 
  while(dataControl == 0){ // Mientras todavía se quiere leer 
  radio.startListening(); // Módulo RF como receptor
  if(radio.available()) // Si hay datos en el pipe
  {
    radio.read(&dataBus, sizeof(dataBus)); // Leer y almacenar en dataBus
    if(dataBus[5] == 1){ // Si el bit 5 de dataBus es 1 (recepción confirmada) 
      dataControl = 1; // Ya no se quiere leer 
      contSec++;
    }
  }
  delay(5); 
  }

  radio.stopListening(); // Módulo RF como transmisor
  dataConfOut[0] = 1; // Se prepara la confirmación 
  radio.write(dataConfOut, sizeof(dataConfOut)); // Se envía la confirmación 

  // Se configuran los parámetros de estimulación dependiendo de lo recibido
  int modo = dataBus[0]; 
  int ancho = dataBus[1]; 
  int tiempo = dataBus[2]; 
  int freq = dataBus[3];
  int sleep = dataBus[4]; 

  // Se muestran en el monitor serial las opciones seleccionadas de los parámetros
  //Serial.print("Reception Number: ");
  //Serial.println(contSec);
  Serial.print("Modo de Operación: ");
  //Serial.print("Operating Mode: ");
  if(modo == 1)
  {
    Serial.println("Estimulación"); 
    //Serial.println("Stimulation"); 
  }
  else if(modo == 2)
  {
    Serial.println("Programación");
    //Serial.println("Programming");
  }
  else if(modo == 3)
  {
    Serial.println("Reposo");
    //Serial.println("Rest");
  }

  Serial.print("Ancho de Pulso: ");
  //Serial.print("Pulse width: "); 
  if(ancho == 1)
  {
    Serial.println("250 us");
  }
  else if(ancho == 2)
  {
    Serial.println("500 us");
  }
  else if(ancho == 3)
  {
    Serial.println("25%");
  }
  else if(ancho == 4)
  {
    Serial.println("50%");
  }
  else if(ancho == 5)
  {
    Serial.println("75%");
  }

  Serial.print("Tiempo de Estimulación: ");
  //Serial.print("ON TIME: ");
  if(tiempo == 1)
  {
    Serial.println("30 s");
  }
  else if(tiempo == 2)
  {
    Serial.println("60 s");
  }
  else if(tiempo == 3)
  {
    Serial.println("Tiempo 3");
  }
  else if(tiempo == 4)
  {
    Serial.println("Tiempo 4");
  }
  else if(tiempo == 5)
  {
    Serial.println("Tiempo 5");
  }

  Serial.print("Frequencia: ");
  //Serial.print("Frequency: "); 
  if(freq == 1)
  {
    Serial.println("490.20 Hz (Default)");
  }
  else if(freq == 2)
  {
    Serial.println("30.64");
  }
  else if(freq == 3)
  {
    Serial.println("122.50 Hz");
  }
  else if(freq == 4)
  {
    Serial.println("245.10 Hz");
  }
  else if(freq == 5)
  {
    Serial.println("980.39 Hz");
  }
  else if(freq == 6)
  {
    Serial.println("3921.16 Hz");
  }
  else if(freq == 7)
  {
    Serial.println("31372.55 Hz");
  }
  else if(freq == 8)
  {
    Serial.println("Frecuencia 8");
  }

  Serial.print("Tiempo de apagado: ");
  //Serial.print("OFF Time: ");
  if(sleep == 1)
  {
    Serial.println("5 min");
  }
  else if(sleep == 2)
  {
    Serial.println("NO");
  }

  Serial.println("");

  dataConfOut[0] = 0; // Se reinicia la confirmación 
  dataControl = 0; // Se pone en lectura otra vez el módulo

  
  
}
