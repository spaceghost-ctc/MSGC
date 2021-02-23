#include <msp430.h>
#include <stdint.h>
#include <SPI.h>

volatile uint8_t spi_buf = 0;

#define SCLK    BIT1
#define MOSI    BIT3
#define MISO    BIT2
#define NSS     BIT0

void spi_txready() {
  while (!(UCA1IFG & UCTXIFG)); // Check to see if TX buffer is available
}

void spi_rxready() {
  while (!(UCA1IFG & UCRXIFG)); // Check to see if RX buffer is available
}

void spi_send(uint8_t data) {
  spi_txready();
  UCA1TXBUF = data;            // Transmit data over SPI from master to slave
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
  P4OUT &= ~NSS;
}

void spi_chipDisable() {
   P4OUT |= NSS;
}
