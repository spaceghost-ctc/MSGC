#include <msp430.h>
#include "uart.h"
#include "mcu.h"

#define RXD    BIT6
#define TXD    BIT7

void uart_init() {
  P1SEL1 &=  RXD;            // P1.6 UCA0RXD input
  P1SEL0 |= ~RXD;
  P1SEL1 &=  TXD;            // P1.7 UCA0TXD output
  P1SEL0 |= ~TXD;

  UCA0CTLW0 |=  UCSWRST;  // USCI Clock = SMCLK,USCI_A0 disabled
  UCA0CTLW0 |= UCSSEL__SMCLK;
  UCA0BR0   =  0x82;                // 0x0682 From datasheet table
  UCA0BR1   =  0x06;                // selects baudrate = 9600bps, clk = SMCLK

  UCA0MCTLW  |= BIT8;             // Modulation value = 1 from datasheet

  UCA0STATW |=  UCLISTEN;            // Loop back mode enabled

  UCA0CTL1 &= ~UCSWRST;             // Clear UCSWRST to enable USCI_A0
}

void uart_write(char* str) {
    int i;
  for(i = 0; str[i] != '\0'; i++) {
    while (!(UCA0IFG & UCTXIFG));    // TX buffer ready?
    UCA0TXBUF = str[i];
  }
}

void uart_writen(char* data, int n) {
  while(n--) {
    while (!(UCA0IFG & UCTXIFG));
    UCA0TXBUF = *data++;
  }
}

void uart_writec(char data) {
  while (!(UCA0IFG & UCTXIFG));
  UCA0TXBUF = data;
}

void uart_printhex8(uint8_t n) {
  char buf[2 + 1];
  char *str = &buf[3 - 1];

  *str = '\0';

  uint8_t base = 16;

  do {
    uint8_t m = n;
    n /= base;
    char c = m - base * n;
    *--str = c < 10 ? c + '0' : c + 'A' - 10;
  } while(n);

  uart_write(str);
}

void uart_printhex32(uint32_t n) {
  char buf[8 + 1];
  char *str = &buf[9 - 1];

  *str = '\0';

  uint32_t base = 16;

  do {
    uint32_t m = n;
    n /= base;
    char c = m - base * n;
    *--str = c < 10 ? c + '0' : c + 'A' - 10;
  } while(n);

  uart_write(str);
}
