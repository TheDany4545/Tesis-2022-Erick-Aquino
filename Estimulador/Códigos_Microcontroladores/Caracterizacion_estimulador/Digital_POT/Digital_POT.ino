/*
   How to use a digital potenciometer with Arduino
*/
#include <SPI.h>

byte address = 0x0011;
int CS = 10;

void setup() {
  pinMode (CS, OUTPUT);
  SPI.begin();
  /*
    pinMode(9, OUTPUT);                               // Set digital pin 9 (D9) to an output
    TCCR1A = _BV(COM1A1) | _BV(WGM11);                // Enable the PWM output OC1A on digital pins 9
    TCCR1B = _BV(WGM13) | _BV(WGM12) | _BV(CS12);     // Set fast PWM and prescaler of 256 on timer 1
    ICR1 = 2082;                                     // Set the PWM frequency to 1Hz: 16MHz/(256 * 1Hz) - 1 = 62499
    OCR1A = 2082*0.55;                                     // valor *%
  */
}

void loop() {
  /*
      digitalPotWrite(38);
      delay(100);

      digitalPotWrite(0);
      delay(100); */

  analogWrite(9, HIGH);
  pinMode(9, OUTPUT);                               // Set digital pin 9 (D9) to an output
  TCCR1A = _BV(COM1A1) | _BV(WGM11);                // Enable the PWM output OC1A on digital pins 9
  TCCR1B = _BV(WGM13) | _BV(WGM12) | _BV(CS12);     // Set fast PWM and prescaler of 256 on timer 1
  ICR1 = 2082;                                     // Set the PWM frequency to 1Hz: 16MHz/(256 * 1Hz) - 1 = 62499
  OCR1A = 2082 * 0.2;
  //
  //ICR1 = 6249;                                     // Set the PWM frequency to 1Hz: 16MHz/(256 * 1Hz) - 1 = 62499
  //OCR1A = 6249 * 0.5;
  // Rampa de Subida
  for (int i = 0; i <= 168; i++) { //168
    digitalPotWrite(i);
    delay(29);
  }
  delay (4000); //segundos de funcionamiento
  //Rampa de Bajada
  for (int i = 168; i >= 0; i--) {
    digitalPotWrite(i);
    delay(29);

  }

  digitalWrite(9, LOW);
  digitalPotWrite(0);
  delay(4000);

}

int digitalPotWrite(int value) {
  digitalWrite(CS, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(CS, HIGH);
}
