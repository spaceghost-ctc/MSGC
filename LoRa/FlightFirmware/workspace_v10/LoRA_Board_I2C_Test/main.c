#include <msp430.h> 

//-----------------Globals-------------------
int Data_In = 0;

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

    UCB1CTLW0 |= UCTR;    // Tx mode
    UCB1I2CSA = 0x2;     // Slave address
    UCB1CTLW1 |= UCASTP_2;   // Auto STOP when UCB1TBCNT reached
    UCB1TBCNT = 0x1;      // Set characters to be send (1 byte)

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

    P4IFG &= ~BIT4; // Clear IRQ Flag
    P4IFG &= ~BIT5; // Clear IRQ Flag
    P4IFG &= ~BIT6; // Clear IRQ Flag
    P4IFG &= ~BIT7; // Clear IRQ Flag

    P1IE |= BIT4;   // Enable IRQ
    P1IE |= BIT5;   // Enable IRQ
    P1IE |= BIT6;   // Enable IRQ
    P1IE |= BIT7;   // Enable IRQ

    __enable_interrupt(); // enable IRQs

    while(1){
        UCB1CTLW0 |= UCTXSTT; // start condition
        while ((UCB1IFG & UCSTPIFG) == 0); // Wait for STOP
            UCB1IFG &= ~UCSTPIFG; // Clear STOP Flag
    }

	return 0;
}

#pragma vector=EUSCI_B1_VECTOR
__interrupt void EUSCI_B1_I2C_ISR(void){

    switch(UCB1IV){
    case 0x16:                  // ID 16: RXIFG1
        Data_In = UCB1RXBUF;
        break;
    case 0x18:                  // ID 18: TX
        //UCB1TXBUF = button;
        break;
    default:
        break;
    }

}
