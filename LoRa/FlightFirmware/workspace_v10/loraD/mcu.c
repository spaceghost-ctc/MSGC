#include <msp430.h>
#include <stdint.h>
#include "mcu.h"

void mcu_init() {
  WDTCTL = WDTPW + WDTHOLD;   // Disable watchdog

  // Setting the DCO see application slaa992.pdf application note 3-1.
  // Disable the FLL.
  // Select ref clock.
  // Clear CSCTL0 reg.
  // Set DCO range and set FLLN and FLLD for target freq
  // Ex NOP 3x
  // EN the FLL
  // Poll FLLUNLOCK until FLL locked
  FRCTL0 = FRCTLPW | NWAITS_1;

      __bis_SR_register(SCG0);                           // disable FLL
      CSCTL3 |= SELREF__REFOCLK;                         // Set REFO as FLL reference source
      CSCTL0 = 0;                                        // clear DCO and MOD registers
      CSCTL1 &= ~(DCORSEL_7);                            // Clear DCO frequency select bits first
      CSCTL1 |= DCORSEL_5;                               // Set DCO = 16MHz
      CSCTL2 = FLLD_0 + 487;                             // DCOCLKDIV = 16MHz
      __delay_cycles(3);
      __bic_SR_register(SCG0);                           // enable FLL
      while(CSCTL7 & (FLLUNLOCK0 | FLLUNLOCK1));         // FLL locked

      CSCTL4 = SELMS__DCOCLKDIV | SELA__REFOCLK;        // set default REFO(~32768Hz) as ACLK source, ACLK = 32768Hz
                                                         // default DCOCLKDIV as MCLK and SMCLK source
  //DCORSEL |= 0b101;     // Set range
  //DCO = 0;     // Set DCO step + modulation

  P1OUT &= 0x00;              // Shut down everything
  P1DIR &= 0x00;
  P2OUT &= 0x00;              // Shut down everything
  P2DIR &= 0x00;
  P3OUT &= 0x00;              // Shut down everything
  P3DIR &= 0x00;
  P4OUT &= 0x00;              // Shut down everything
  P4DIR &= 0x00;
  P5OUT &= 0x00;              // Shut down everything
  P5DIR &= 0x00;
  P6OUT &= 0x00;              // Shut down everything
  P6DIR &= 0x00;
}

void mcu_delayms(uint32_t ms) {
  while (ms) {
    __delay_cycles(16 * 998);
  	ms--;
  }
}

void mcu_delayus(uint32_t us) {
	while (us) {
		__delay_cycles(14); //for 16MHz
		us--;
  }
}

void mcu_memcpy1(uint8_t *dst, const uint8_t *src, uint16_t size) {
    while(size--) *dst++ = *src++;
}
