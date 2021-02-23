#include <msp430.h>
#include <stdint.h>
#include "inst.h"

#define SCLK    BIT1
#define MOSI    BIT3
#define MISO    BIT2
#define NSS     BIT0

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
