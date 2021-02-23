#include <msp430.h> 
#include <inst.h>
#include <stdint.h>
#include <SPI.h>
#include <RFM69_REG.h>

int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	
	mcu_init();

    PM5CTL0 &= ~LOCKLPM5;       //  GPIO on

	TB0CTL |= TBIE;             //  Local Enable for TB0 Overflow
	__enable_interrupt();       //  Enable Maskable IRQs
	TB0CTL &= ~TBIFG;           //  Clear IRQ Flag

	while(1){}                  //  Run Forever

	return 0;
}

#pragma vector = TIMER0_B1_VECTOR
__interrupt void ISR_TB0_Overflow(void){
    P6OUT ^= BIT0;             //  LED 1 toggles
//    P6OUT ^= BIT1;             //  LED 2 toggles
//    P6OUT ^= BIT2;             //  LED 3 toggles
    spi_send(0x80);
    spi_send(0xFF);
    spi_send(0x80);
    spi_send(0xAA);
    spi_send(0x80);
    spi_send(0x00);
    spi_send(0x80);
    spi_send(0x55);
    TB0CTL &= ~TBIFG;
}
