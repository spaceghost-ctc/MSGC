#include <msp430.h> 

#define SCLK    BIT1
#define MOSI    BIT3
#define MISO    BIT2
#define NSS     BIT0
/**
 * main.c
 * version 1.1
 * Recievable by GS, only 0s though
 */
char registerStats[11];
char transmitted,transmitted1,transmitted2,transmitted3;

char txpack[256];

void delay(unsigned int j){
    unsigned int k;
    for(k = 0; k < j; k++){
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

    delay(10000);

    unsigned int i;
    for(i=0;i<256;i++){
        txpack[i]=0xAA;
    }
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x81;
        UCA1TXBUF = 0x80;       //  Register Operation mode set to Sleep LoRa
        delay(20);
        P4OUT |= NSS;
        delay(20); // delay to ensure we are in sleep  mode
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x8E;       //  Set FIFO Tx Addr
        UCA1TXBUF = 0x00;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x8F;       //  Set FIFO Rx Addr
        UCA1TXBUF = 0x00;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x81;
        UCA1TXBUF = 0x81;       //  Set to Standby LoRa
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x86;       //  Set to 912 MHz MSB
        UCA1TXBUF = 0xE4;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x87;       // Set to 912 MHz MidSB
        UCA1TXBUF = 0x00;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x88;       //  Set to 912 MHz LSB
        UCA1TXBUF = 0x00;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x89;       //  Set Power Output
        UCA1TXBUF = 0x8F;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0xA0;       //  Set Preamble MSB
        UCA1TXBUF = 0x00;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0xA1;       //  Set Preamble LSB
        UCA1TXBUF = 0x08;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x9D;
        UCA1TXBUF = 0x72;       //  Set to BWIE Reg Modem Config 1
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x9E;       //  Reg Modem Config 2
        UCA1TXBUF = 0xA4;
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0xA6;
        UCA1TXBUF = 0x00;       	// CHANGED FROM 0x04 Set Reg Modem Config 3
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0x81;
        UCA1TXBUF = 0x81;       	//  Set to Standby LoRa
        delay(20);
        P4OUT |= NSS;
        P4OUT &= ~NSS;
        UCA1TXBUF = 0xA2;
        UCA1TXBUF = 0x1F;       	//  Set to Payload Leng LoRa
        delay(20);
        P4OUT |= NSS;


//        P4OUT &= ~NSS;
//        UCA1TXBUF = 0x91;
//        UCA1TXBUF = 0x80;       	//  Set to Int on Tx
//        delay(20);
//        P4OUT |= NSS;



        unsigned int j,k;           //  Reading first 10 registers
        k = 0;
        for(j = 0x01; j < 0x0A; j++){
            P4OUT &= ~NSS;
            UCA1TXBUF = j;
            UCA1TXBUF = 0x00;
            registerStats[k] = UCA1RXBUF;
            delay(20);
            P4OUT |= NSS;
            k++;
            delay(5);
        }

        while(1){
            P6OUT ^= BIT0;              //  Toggle LED1
            P4OUT &= ~NSS;
            UCA1TXBUF = 0x8D;
            UCA1TXBUF = 0x00;       	//  Set Pointer to FIFO LoRa
            delay(20);
            P4OUT |= NSS;

			P4OUT &= ~NSS;
			UCA1TXBUF = 0x0D;
			UCA1TXBUF = 0x0D;
			transmitted2 = UCA1RXBUF;
			delay(20);
			P4OUT |= NSS;

			P4OUT &= ~NSS;
			UCA1TXBUF = 0x0E;
			UCA1TXBUF = 0x0E;
			transmitted3 = UCA1RXBUF;
			delay(20);
			P4OUT |= NSS;

            P4OUT &= ~NSS;
            UCA1TXBUF = 0x80;           // Write + FIFO Transmit register (1 + 0000000)
            UCA1TXBUF = 0xFC;			//	Header to
            UCA1TXBUF = 0XFB;			//	Header from
            UCA1TXBUF = 0x00;
            UCA1TXBUF = 0x00;
            UCA1TXBUF = 0xFF;
            UCA1TXBUF = 0x00;
            UCA1TXBUF = 0xAA;
            UCA1TXBUF = 0x00;
            UCA1TXBUF = 0xFF;
            UCA1TXBUF = 0x00;
            UCA1TXBUF = 0x55;
            UCA1TXBUF = 0x00;
            UCA1TXBUF = 0xFF;
            UCA1TXBUF = 0x00;
            delay(150);
            P4OUT |= NSS;

//            P4OUT &= ~NSS;
//            UCA1TXBUF = 0x8D;
//            UCA1TXBUF = 0x00;       	//  Set Pointer to FIFO LoRa
//            delay(20);
//            P4OUT |= NSS;

			P4OUT &= ~NSS;
			UCA1TXBUF = 0x0D;
			UCA1TXBUF = 0x0D;
			transmitted = UCA1RXBUF;
			delay(20);
			P4OUT |= NSS;

            P4OUT &= ~NSS;
            UCA1TXBUF = 0x81;
            UCA1TXBUF = 0x83;       	//  Set to Transmit LoRa
            delay(20);
            P4OUT |= NSS;

				P4OUT &= ~NSS;
				UCA1TXBUF = 0x0E;
				UCA1TXBUF = 0x0E;
				transmitted1 = UCA1RXBUF;
				delay(20);
				P4OUT |= NSS;
//
//            P4OUT &= ~NSS;
//            UCA1TXBUF = 0x81;
//            UCA1TXBUF = 0x81;       	//  Set to Standby LoRa
//            delay(20);
//            P4OUT |= NSS;

//            for(i=0;i<50;i++){
//            	delay(10000);
//            }

        }

}
