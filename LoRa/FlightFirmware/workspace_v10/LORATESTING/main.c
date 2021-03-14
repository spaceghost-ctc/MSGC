#include <msp430.h> 

/* @Title: MSP4302355 to RFM95 LoRa Radio
 * @Author: Larson Brandstetter
 * @Version: v1.0
 *
 * @Description: This version lays out the primary communication between the LoRa Radio Transmitter and the MSP430 Microcontroller over SPI.
 *
 */

#define SCLK    BIT1
#define MOSI    BIT3
#define MISO    BIT2
#define NSS     BIT0

char registerStats[10];
char reg;
unsigned int start;

void delay(unsigned int j){
    unsigned int i;
    for(i = j; i > 0; i--){
        P6OUT ^= BIT2;              //  Toggle LED3
    }
}

void registerSet(){         // Setting up the LoRa
    P4OUT &= ~NSS;
    UCA1TXBUF = 0x81;       // Register Operation Mode set to Sleep
    UCA1TXBUF = 0x00;
    delay(20);
    P4OUT |= NSS;
    P4OUT &= ~NSS;
    UCA1TXBUF = 0x81;
    UCA1TXBUF = 0x80;       //  Register Operation mode set to LoRa
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
    UCA1TXBUF = 0x89;       //  Set to 900 MHz LSB
    UCA1TXBUF = 0x00;
    delay(20);
    P4OUT |= NSS;
    P4OUT &= ~NSS;
    UCA1TXBUF = 0x89;
    UCA1TXBUF = 0xFF;       //  Max power output
    delay(20);
    P4OUT |= NSS;
    P4OUT &= ~NSS;
    UCA1TXBUF = 0x9D;
    UCA1TXBUF = 0x02;       //  Minimum Bandwidth
    delay(20);
    P4OUT |= NSS;
}

void registerCheck(){
    unsigned int j,k;
    k = 0;
    for(j = 0x01; j < 0x09; j++){
        P4OUT &= ~NSS;
        UCA1TXBUF = j;
        UCA1TXBUF = 0x00;
        registerStats[k] = UCA1RXBUF;
        delay(20);
        P4OUT |= NSS;
        k++;
        delay(5);
    }
}

void sendData(){
    P4OUT &= ~NSS;
    UCA1TXBUF = 0x81;
    UCA1TXBUF = 0x83;       //  Set to Transmit LoRa
    delay(20);
    P4OUT |= NSS;
    unsigned int j;
    P4OUT &= ~NSS;
    UCA1TXBUF = 0x80;           // Write + FIFO Transmit register (1 + 0000000)
    for(j=255;j>0;j--){
        UCA1TXBUF = j;
        delay(10);
    }
    P4OUT |= NSS;
    P4OUT &= ~NSS;
    UCA1TXBUF = 0x81;
    UCA1TXBUF = 0x81;       //  Set to Standby LoRa
    delay(20);
    P4OUT |= NSS;
}

int main(void)
{
    WDTCTL = WDTPW | WDTHOLD;   // stop watchdog timer

    //  INITIALIZING uController with SPI, UART, I2C, and Timers

    //  INITIALIZING SPI
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

    //  Initial Conditions
    start = 0;
    reg = 0;
    P4OUT |= NSS;

    while(1){
        delay(10000);           //  Startup Delay for LoRa
        unsigned int j;
        if(start == 0){
            registerSet();      //  Sets Register Status and Device Operation Modes
            start = 1;
        }
        else if(reg == 0){
            registerCheck();    //  Displays Register Status for Debugging (Not Necessary for Distribution)
            reg = 1;
        }
        else{
            sendData();         //  Sends Assembled Data Packet
        }
        P6OUT ^= BIT1;          //  Toggle LED2 every time the SPI is finished
        for(j=15;j>0;j--){
            delay(10000);
        }
        P6OUT ^= BIT1;          //  Toggle LED2 every time the delay is finished and SPI is ready
    }

    return 0;
}
