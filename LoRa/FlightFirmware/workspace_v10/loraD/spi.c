#include <msp430.h>
#include <stdint.h>
#include "spi.h"

volatile uint8_t spi_buf = 0;

#define SCLK    BIT1
#define SDI     BIT3
#define SDO     BIT2
#define CS      BIT0

//#define INT1    BIT4
//#define INT2    BIT3

void spi_init() {
  UCA1CTLW0 = UCSWRST;
  UCA1CTLW0 |= UCSYNC;
  UCA1CTLW0 |= UCMST; //UCMSB + UCMST + UCSYNC; // 3-pin, 8-bit SPI master
  UCA1CTLW0 |= UCMODE1;
  UCA1CTLW0 &= ~UCMODE0;

  UCA1CTLW0 |= UCSSEL__SMCLK;                         // SMCLK
  UCA1BRW = 10;                               // Frequency CPU / 2 (16Mhz / 2 = 8 Mhz SPI)

  UCA1CTLW0 |= UCSTEM;

  P4SEL1 &= ~SCLK;  // P4.1 SCLK
  P4SEL0 |= SCLK;

  P4SEL1 &= ~SDI;  // P4.3 SIMO
  P4SEL0 |= SDI;

  P4SEL1 &= ~SDO;  //P4.2 SOMI
  P4SEL0 |= SDO;

  P4SEL1 &= ~CS; //P4.0 NSS/STE
  P4SEL0 |= CS;

  //P1DIR &= ~(INT1 | INT2);                      // P1.4 and P1.3 as INT (INTERRUPT, not used yet)

  UCA1CTLW0 &= ~UCSWRST;                         // Initialize USCI state machine
}

void spi_txready() {
  while (!(UCA1IFG & UCTXIFG)); // TX buffer ready?
}

void spi_rxready() {
  while (!(UCA1IFG & UCRXIFG)); // RX Received?
}

void spi_send(uint8_t data) {
  spi_txready();
  UCA1TXBUF = data;            // Send data over SPI to Slave
}

void spi_recv() {
  spi_rxready();
  spi_buf = UCA1RXBUF;         // Store received data
}

void spi_transfer(uint8_t data) {
  spi_send(data);
  spi_recv();
}

void spi_chipEnable() {
  P2OUT &= ~CS;
}

void spi_chipDisable() {
   P2OUT |= CS;
}
