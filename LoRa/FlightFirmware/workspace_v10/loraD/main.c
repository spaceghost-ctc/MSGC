#include <msp430.h> 

int Rx_Data;

int main(void){
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	
	UCA0CTLW0 |= UCSWRST;

	UCA0CTLW0 |= UCSSEL__SMCLK;
	UCA0BRW = 10;

	UCA0CTLW0 |= UCSYNC;
	UCA0CTLW0 |= UCMST;

	P1SEL1 &= ~BIT5;  // P1.5 SCLK
	P1SEL0 |= BIT5;

    P1SEL1 &= ~BIT7;  // P1.7 SIMO
    P1SEL0 |= BIT7;

    P1SEL1 &= ~BIT6;  //P1.6 SOMI
    P1SEL0 |= BIT6;

	PM5CTL0 &= ~LOCKLPM5;

	UCA0CTLW0 &= ~UCSWRST;

	UCA0IE |= UCRXIE;
	UCA0IFG &= ~UCRXIFG;

	__enable_interrupt();

	int i;

	while(1){
	    UCA0TXBUF = 0x4D;
	    for(i=10000;i>0;i--){}
	}

	return 0;
}

#pragma vector = EUSCI_A0_VECTOR
__interrupt void ISR_EUSCI_A0(void){
    Rx_Data = UCA0RXBUF;

}
