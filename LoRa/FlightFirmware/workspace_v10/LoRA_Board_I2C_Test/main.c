#include <msp430.h> 

//-----------------Globals-------------------
int data_in = 0;
int data_out = 0;
int i;
int data_rec = 0;
int data_tran = 0;

//------------------Functions---------------------------------------------------------------------
void transmit_I2C(void){
    UCB1CTLW0 |= UCTR;    // TX mode
    data_out = 0x0A;
    UCB1CTLW0 |= UCTXSTT; // start condition
    while ((UCB1IFG & UCSTPIFG) == 0); // Wait for STOP
    UCB1IFG &= ~UCSTPIFG; // Clear STOP Flag
}

/**
 * main.c
 */
int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	
//------------------Configure I2C Master Mode---------------------------------------------------------------------
	//------ 1. Software Reset
	UCB1CTLW0 |= UCSWRST;   // UCSWRST = 1 for SW reset

    //------ 2. Configure eUSCI_B0
    UCB1CTLW0 |= UCSSEL_3;   // 1MHz clock
    UCB1BRW = 100;           // Divide by 10 to get 100kHz
    UCB1CTLW0 |= UCMODE_3;   // Put into I2C mode
    UCB1CTLW0 |= UCMST;      // Put into master mode

    //UCB1CTLW0 &= ~UCTR;    // RX mode
    UCB1I2CSA = 0x4A;     // Slave address for temp sensor

    //UCB1CTLW0 |= UCTR;    // TX mode
    UCB1CTLW1 |= UCASTP_0;   // DO NOT Auto STOP when UCB1TBCNT reached
    //UCB1CTLW1 |= UCASTP_2;   // Auto STOP when UCB1TBCNT reached
    UCB1TBCNT = 0x2;      // Set characters to be send (1 byte)

    //------ 3. Configure Ports
    P4SEL1 &= ~BIT7;        // P4.7 is SCL
    P4SEL0 |= BIT7;
    P4SEL1 &= ~BIT6;        // P4.6 is SDA
    P4SEL0 |= BIT6;

    PM5CTL0 &= ~LOCKLPM5; // Turn on GPIO

    //------ 4. Take out of SW reset
    UCB1CTLW0 &= ~UCSWRST;

	//------ 5. Enable Interrupts
    UCB1IE |= UCTXIE; // Tx0 IRQ
    UCB1IE |= UCRXIE; // Rx0 IRQ

    P4IFG &= ~BIT6; // Clear IRQ Flag
    P4IFG &= ~BIT7; // Clear IRQ Flag

    P4IE |= BIT6;   // Enable IRQ
    P4IE |= BIT7;   // Enable IRQ

    __enable_interrupt(); // enable IRQs

    while(1){

        /*//Pressure
        UCB1I2CSA = 0x77;
        UCB1TBCNT = 0x1;
        UCB1CTLW0 |= UCTR;    // TX mode
        data_out = 0x1E;
        for(i = 0; i < 100; i++){}
        transmit_I2C();
        data_out = 0x40;
        for(i = 0; i < 100; i++){}
        transmit_I2C();
        data_out = 0x00;
        for(i = 0; i < 100; i++){}
        transmit_I2C();
        UCB1TBCNT = 0x3;
        UCB1CTLW0 &= ~UCTR;    // RX mode
        for(i = 0; i < 1500; i++){}
        transmit_I2C();*/

        //Temperature
        transmit_I2C();
        data_rec = 0;
        data_tran = 0;
    }

	//return 0;
}

#pragma vector=EUSCI_B1_VECTOR
__interrupt void EUSCI_B1_I2C_ISR(void){

    switch(UCB1IV){
    case 0x16:                  // ID 16: RX
        if(data_rec == 0){
            data_in = UCB1RXBUF;
            data_rec = 1;
        }
        break;
    case 0x18:                  // ID 18: TX
        if(data_tran == 0){
            UCB1TXBUF = data_out;
            data_tran = 1;
        }else if(data_tran == 1){
            UCB1CTLW0 &= ~UCTR;
            UCB1CTLW0 |= UCTXSTT; // start condition
            while((UCB1CTLW0 & UCTXSTT));
            UCB1CTLW0 |= UCTXSTP; // stop condition
        }
        break;
    default:
        break;
    }
}
