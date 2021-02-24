#include <msp430.h>
#include <stdint.h>
#include "inst.h"

#define SCLK    BIT1
#define MOSI    BIT3
#define MISO    BIT2
#define NSS     BIT0

#define RXD    BIT6
#define TXD    BIT7

void mcu_init() {
    //  INITIALIZING uController with SPI, UART, I2C, and Timers
    //  INITIALIZING SPI
    UCA1CTLW0 = UCSWRST;        //  Placing UCA1CTLW0 into SW reset
    UCA1CTLW0 |= UCSTEM;        //  STE set to Enable 4-pin mode
    UCA1CTLW0 |= UCSSEL__SMCLK; //  Clock set to SMCLK
    UCA1CTLW0 |= UCSYNC;        //  Synchronous Mode
    UCA1CTLW0 |= UCMODE1;       //  4-Pin SPI with UCxSTE active low
    UCA1CTLW0 &= ~UCMODE0;      //  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    UCA1CTLW0 |= UCMST;         //  SPI Master
    UCA1CTLW0 |= UC7BIT;        //  8-bit Character Length
    UCA1CTLW0 |= UCMSB;         //  MSB first
                                //  Settings from eUSCI - SPI Mode Excerpt from SLAU208 Texas Instruments

    P4SEL1 &= ~SCLK;            // P4.1 SCLK
    P4SEL0 |= SCLK;

    P4SEL1 &= ~MOSI;            // P4.3 SIMO
    P4SEL0 |= MOSI;

    P4SEL1 &= ~MISO;            //P4.2 SOMI
    P4SEL0 |= MISO;

    P4SEL1 &= ~NSS;             //P4.0 NSS/STE
    P4SEL0 |= NSS;

    UCA1CTLW0 &= ~UCSWRST;      // SPI operation Ready


    //  INITIALIZING UART
    UCA0CTLW0 = UCSWRST;        //  Placing UCA0CTLW0 into SW reset
    UCA0CTLW0 |= UCSSEL__SMCLK;
    UCA0CTLW0 |= UCSYNC;
    UCA0CTLW0 |= UCSPB;         //  Two stop bits
    UCA0CTLW0 |= UC7BIT;        //  8-bit mode
    UCA0CTLW0 |= UCMSB;         //  MSB first
    UCA0BR0 |= 0x82;            //  Baud rate set to 9600 on SMCLK
    UCA0BR1 |= 0x06;

    P1SEL1 &=  RXD;            // P1.6 UCA0RXD input
    P1SEL0 |= ~RXD;
    P1SEL1 &=  TXD;            // P1.7 UCA0TXD output
    P1SEL0 |= ~TXD;

    UCA0CTLW0 &= ~UCSWRST;      //  UART operation Ready
    //  INITIALIZING I2C
    //  INITIALIZING CLOCK
    //  OTHER PORTS
    TB0CTL |= TBCLR;            //  RESET timer
    TB0CTL |= TBSSEL__ACLK;     //  Timer set to ACLK
    TB0CTL |= MC__CONTINUOUS;   //  Continuous Mode


    P6DIR |= BIT0;              //  LED 1 on Port 6.0 as output
    P6OUT &= ~BIT0;             //  LED off initially

    P6DIR |= BIT1;              //  LED 2 on Port 6.1 as output
    P6OUT &= ~BIT1;             //  LED off initially

    P6DIR |= BIT2;              //  LED 3 on Port 6.2 as output
    P6OUT &= ~BIT2;             //  LED off initially

}
