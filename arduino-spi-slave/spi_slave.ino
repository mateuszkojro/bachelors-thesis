#include <SPI.h>
#include <avr/sleep.h>

void setup(void) {
  // We are a slave MISO needs to be an output
  pinMode(MISO, OUTPUT);
  // Enable SPI in slave mode
  SPCR |= _BV(SPE);
  // Enable interrupts
  SPCR |= _BV(SPIE);
  
  // Message that will be transfered 
  // with the first interaction
  SPDR = 66;

  set_sleep_mode(SLEEP_MODE_IDLE);
}

// Interupt that will be run when a new message comes
ISR (SPI_STC_vect) {
  // Respond with the message that came in
  byte copy = SPDR;
  SPDR = copy; 
}

void loop (void) {
  sleep_mode();
}