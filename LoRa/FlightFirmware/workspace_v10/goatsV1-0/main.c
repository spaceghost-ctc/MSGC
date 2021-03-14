#include <msp430.h> 

#define SCLK    BIT1
#define MOSI    BIT3
#define MISO    BIT2
#define NSS     BIT0
/**
 * main.c
 * version 1
 */
char registerStats[11];

char txpack[256];

void delay(unsigned int j){
    unsigned int i;
    for(i = j; i > 0; i--){
        P6OUT ^= BIT2;              //  Toggle LED3
    }
}

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;   // stop watchdog timer

    UCA1CTLW0 = UCSWRST;        //  Placing UCA1CTLW0 into SW reset
    UCA1CTLW0 |= UCSSEL__SMCLK; //  Clock set to SMCLK 1MHz
    UCA1BRW = 10;               //  Divide down to 100kHz
    UCA1CTLW0 |= UCSYNC;        //  Synchronous Mode
    UCA1CTLW0 |= UCMST;         //  SPI Master
    UCA1CTLW0 |= UCMSB;         //  MSB first
                                //  Settings from eUSCI - SPI Mode Excerpt from SLAU208 Texas Instruments
    //  SPI PORTS
    P4SEL1 &= ~SCLK;            //  P4.1 SCLK
    P4SEL0 |= SCLK;
    P4SEL1 &= ~MOSI;            //  P4.3 SIMO
    P4SEL0 |= MOSI;
    P4SEL1 &= ~MISO;            //  P4.2 SOMI
    P4SEL0 |= MISO;
    P4DIR |= NSS;               //  P4.0 NSS/STE (Manually Toggled)

    //  OTHER PORTS
    P6DIR |= BIT0;              //  LED 1 on Port 6.0 as output
    P6OUT |= BIT0;              //  LED off initially

    P6DIR |= BIT1;              //  LED 2 on Port 6.1 as output
    P6OUT |= BIT1;              //  LED off initially

    P6DIR |= BIT2;              //  LED 3 on Port 6.2 as output
    P6OUT |= BIT2;              //  LED off initially

    UCA1CTLW0 &= ~UCSWRST;      //  SPI operation Ready

    PM5CTL0 &= ~LOCKLPM5;       //  GPIO on

    P4OUT |= NSS;               //  Turn off Chip Select

    delay(1000);

    unsigned int i;
    for(i=0;i<256;i++){
        txpack[i]=0xAA;
    }
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x81;       // Register Operation Mode set to Sleep
        UCA1TXBUF = 0x00;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x81;
        UCA1TXBUF = 0x0C;       //  Register Operation mode set to LoRa
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x81;
        UCA1TXBUF = 0x83;       //  Set to Transmit LoRa
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x86;       //  Set to 900 MHz MSB
        UCA1TXBUF = 0xE1;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x87;       // Set to 900 MHz MidSB
        UCA1TXBUF = 0x00;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x88;       //  Set to 900 MHz LSB
        UCA1TXBUF = 0x00;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x89;       //  Set to 900 MHz LSB
        UCA1TXBUF = 0x8F;
        delay(20);
        P4OUT |= NSS;




//        unsigned int j,k;           //  Reading first 10 registers
//        k = 0;
//        for(j = 0x01; j < 0x0A; j++){
//            P4OUT &= ~NSS;
//            UCA1TXBUF = j;
//            UCA1TXBUF = 0x00;
//            registerStats[k] = UCA1RXBUF;
//            delay(20);
//            P4OUT |= NSS;
//            k++;
//            delay(5);
//        }

        while(1){
            P4OUT &= ~NSS;
            UCA1TXBUF = 0x81;
            UCA1TXBUF = 0x83;       //  Set to Transmit LoRa
            delay(20);
            P4OUT |= NSS;
            P4OUT &= ~NSS;
            UCA1TXBUF = 0x80;           // Write + FIFO Transmit register (1 + 0000000)
            for(i=0;i<256;i++){
                UCA1TXBUF = 0xaa;
                delay(10);
            }
            P4OUT |= NSS;

            delay(10000);
            delay(1);
        }

	//return 0;
}
