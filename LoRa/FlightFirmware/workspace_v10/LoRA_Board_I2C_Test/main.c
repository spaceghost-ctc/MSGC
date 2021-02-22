#include <msp430.h> 

#define TEMP 0
#define PRESSURE 1
#define GET_PRESSURE_COEFFS 2
#define ACCEL 3
#define EXT_TEMP_ADDR 0x4A
#define INT_TEMP_ADDR 0x4B
#define RECEIVE 0
#define SEND 1
#define CONV_PRESSURE 0x48
#define CONV_TEMP 0x58

//-----------------Globals-------------------
short data_in = 0;
short data_out = 0;
unsigned int i;
char I2C_sensor_case = TEMP; //0 = temp, 1 = pressure, 2 = get pressure coefficients, 3 = accelerometer
char data_rec = 0;
char data_tran = 0;
char temp_I2C_flag = 0;
char send_rec;
char j;
unsigned char crc;
int temp_ext;
int temp_int;
long pressure = 0;
long press_temp = 0;
unsigned long digital_pressure_temp = 0;
unsigned long digital_pressure = 0;
//---pressure coefficients for calculation
unsigned int coeffs[8]; // [blank, SENST1, OFFT1, TCS, TCO, TREF, TEMPSENSE, CRC bit]

//------------------Functions---------------------------------------------------------------------
void transmit_I2C(void){
    UCB1CTLW0 |= UCTXSTT; // start condition
    if((I2C_sensor_case == PRESSURE || I2C_sensor_case == GET_PRESSURE_COEFFS) && send_rec == RECEIVE){
        UCB1IFG |= UCRXIFG0;
    }
    while ((UCB1IFG & UCSTPIFG) == 0); // Wait for STOP
    UCB1IFG &= ~UCSTPIFG; // Clear STOP Flag
}

int get_temperature(char addr){

    int temp = 0;
    I2C_sensor_case = TEMP;
    UCB1I2CSA = addr;
    temp_I2C_flag = 1;
    data_out = 0x00;
    UCB1CTLW0 |= UCTR;    // TX mode
    transmit_I2C();
    temp = data_in;
    temp = temp << 8;
    data_out = 0x01;
    data_rec = 0;
    data_tran = 0;
    UCB1CTLW0 |= UCTR;    // TX mode
    transmit_I2C();
    temp = temp + data_in;
    data_rec = 0;
    data_tran = 0;
    temp_I2C_flag = 0;

    return temp;
}

void read_pressure_sens(int data){
    I2C_sensor_case = PRESSURE;
    UCB1I2CSA = 0x77;
    UCB1CTLW0 |= UCTR;    // TX mode

    send_rec = SEND;

    data_out = data;
    transmit_I2C();
    for(i = 0; i < 900; i++){}
    data_tran = 0;

    data_out = 0x00;
    transmit_I2C();
    for(i = 0; i < 200; i++){}
    data_tran = 0;

    send_rec = RECEIVE;

    //UCB1TBCNT = 0x3; //set characters to recieve (3 bytes)
    digital_pressure_temp = 0;
    UCB1CTLW0 &= ~UCTR;    // RX mode
    transmit_I2C();
    data_rec = 0;
    for(i = 0; i < 100; i++){}

}

void get_pressure_coeff(int coeff){
    I2C_sensor_case = PRESSURE;
    data_out = coeff;
    send_rec = SEND;
    UCB1CTLW0 |= UCTR;    // TX mode
    transmit_I2C();
    data_tran = 0;
    for(i = 0; i < 500; i++){}

    I2C_sensor_case = GET_PRESSURE_COEFFS;
    if(coeff != 0xA2 || temp_I2C_flag == 1){
        send_rec = RECEIVE;
        temp_I2C_flag = 1;
    }
    UCB1CTLW0 &= ~UCTR;    // RX mode
    transmit_I2C();
    data_rec = 0;
    for(i = 0; i < 500; i++){}
}

void reset_pressure(void){
    I2C_sensor_case = PRESSURE;
    UCB1I2CSA = 0x77;
    UCB1CTLW0 |= UCTR;    // TX mode

    send_rec = SEND;

    data_out = 0x1E;
    for(i = 0; i < 500; i++){}
    transmit_I2C();
    data_tran = 0;
    for(i = 0; i < 350; i++){}

    for(j = 0; j < 8; j++){
    get_pressure_coeff((0xA0+j*2));
    coeffs[j] = data_in;
    }
}

void calculate_pressure(void){
    long dT;
    long OFF;
    long SENS;
    long temp;



}


/**
 * main.c
 */
int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer

    PM5CTL0 &= ~LOCKLPM5; // Turn on GPIO

    P4SEL1 &= ~BIT7;        // P4.7 is GPIO
    P4SEL0 &= ~BIT7;         // ...
    //P4SEL1 &= ~BIT6;        // P4.6 is GPIO
    //P4SEL0 &= ~BIT6;         // ...

    P4DIR |= BIT7;          //Temporarily set 7 to output
    P4OUT &= ~BIT7;          // set P2.6 pin to high as to clear clock on reset
    //P4DIR |= BIT6;          //Temporarily set 6 to output
    //P4OUT |= BIT6;          // set P2.7 pin to high as to clear data on reset

    for(i = 0; i < 200; i++){}

    PM5CTL0 |= LOCKLPM5; // Turn on GPIO

//------------------Configure I2C Master Mode---------------------------------------------------------------------
	//------ 1. Software Reset
	UCB1CTLW0 |= UCSWRST;   // UCSWRST = 1 for SW reset

    //------ 2. Configure eUSCI_B0
    UCB1CTLW0 |= UCSSEL_3;   // 1MHz clock
    UCB1BRW = 100;           // Divide by 10 to get 100kHz
    UCB1CTLW0 |= UCMODE_3;   // Put into I2C mode
    UCB1CTLW0 |= UCMST;      // Put into master mode

    //UCB1CTLW0 &= ~UCTR;    // RX mode
    //UCB1I2CSA = 0x4A;     // Slave address for temp sensor

    //UCB1CTLW0 |= UCTR;    // TX mode
    UCB1CTLW1 |= UCASTP_0;   // DO NOT Auto STOP when UCB1TBCNT reached
    //UCB1CTLW1 |= UCASTP_2;   // Auto STOP when UCB1TBCNT reached
    //UCB1TBCNT = 0x3;      // Set characters to be send (1 byte)

    //------ 3. Configure Ports
    P4SEL1 &= ~BIT7;        // P4.7 is SCL
    P4SEL0 |= BIT7;
    P4SEL1 &= ~BIT6;        // P4.6 is SDA
    P4SEL0 |= BIT6;

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

    reset_pressure();

    while(1){

        //Temperature
        //temp_ext = get_temperature(EXT_TEMP_ADDR);
        //temp_int = get_temperature(INT_TEMP_ADDR);

        //Pressure
        read_pressure_sens(CONV_PRESSURE);
        digital_pressure = (digital_pressure_temp & 0x00FFFFFF);
        read_pressure_sens(CONV_TEMP);
        digital_pressure_temp = (digital_pressure_temp & 0x00FFFFFF);
        calculate_pressure();
        for(i = 0; i < 10; i++){}
    }

	//return 0;
}

#pragma vector=EUSCI_B1_VECTOR
__interrupt void EUSCI_B1_I2C_ISR(void){

    switch(UCB1IV){
    case 0x16:                  // ID 16: RX
        switch(I2C_sensor_case){
        case TEMP:
            if(data_rec == 0){
                data_in = UCB1RXBUF;
                data_rec = 1;
            }
            break;
        case PRESSURE:
            if(data_rec < 3){
                digital_pressure_temp = digital_pressure_temp + UCB1RXBUF;
                digital_pressure_temp = digital_pressure_temp << 8;
                data_rec++;
            }else if(data_rec == 3){
                digital_pressure_temp = digital_pressure_temp + UCB1RXBUF;
                data_rec++;
                UCB1CTLW0 |= UCTXSTP; // stop condition
            }
            break;
        case GET_PRESSURE_COEFFS:
            if(data_rec == 0){
                data_in = UCB1RXBUF;
                data_in = data_in << 8;
                data_rec++;
            }else if(data_rec == 1){
                data_in = data_in + UCB1RXBUF;
                data_rec++;
                UCB1CTLW0 |= UCTXSTP; // stop condition
            }
            break;
        default:
            break;
        }
        break;

    case 0x18:                  // ID 18: TX
        switch(I2C_sensor_case){
        case TEMP:
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
        case PRESSURE:
            if(data_tran == 0){
                UCB1TXBUF = data_out;
                data_tran = 1;
            }else if(data_tran == 1){
                UCB1CTLW0 |= UCTXSTP; // stop condition
            }
            break;
        default:
            break;
        }
        break;

    default:
        break;

    }
}
