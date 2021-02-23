#include <msp430.h> 
#define SCL BIT7
#define SDA BIT6
#define WRITE_MODE 0
#define READ_MODE 1
#define EXT_TEMP_ADDR 0x4A
#define INT_TEMP_ADDR 0x4B
#define NAK_FLAG 0x01
#define I2C_DELAY 10

//--------------Globals--------------------
char i, j;
char i2c_status = 0x00; // 0b00000000 -- | 0 | 0 | 0 | 0 || 0 | 0 | 0 | 1-NAK |
int int_temp = 0;

//--------------Functions--------------------

void i2c_clock_cycle(void){
    P4OUT |= SCL; //SCL HIGH
    for(j=I2C_DELAY; j!=0; j--){}
    P4OUT &= ~SCL; //SCL LOW
}

void i2c_tx_high_bit(void){
    P4OUT |= SDA; //SDA HIGH
    //toggle clock
    i2c_clock_cycle();
}

void i2c_tx_low_bit(void){
    P4OUT &= ~SDA; //SDA LOW
    //toggle clock
    i2c_clock_cycle();
}

void i2c_start(void){
    P4OUT |= SCL; //SCL HIGH
    P4OUT &= ~SDA; //SDA LOW
    for(j=I2C_DELAY; j!=0; j--){}
    P4OUT &= ~SCL; //SCL LOW
}

void i2c_stop(void){
    P4OUT &= ~SDA; //SDA LOW
    for(j=I2C_DELAY; j!=0; j--){}
    P4OUT |= SCL; //SCL HIGH
    for(j=I2C_DELAY; j!=0; j--){}
    P4OUT |= SDA; //SDA HIGH
}

void i2c_nack(void){
    P4OUT |= SDA; //SDA HIGH
    for(j=I2C_DELAY; j!=0; j--){}
    i2c_clock_cycle();
    P4OUT &= ~SDA; //SDA LOW
}

void i2c_read_ack(void){
    P4DIR &= ~SDA; // SDA input port
    for(j=I2C_DELAY*3; j!=0; j--){}
    if(P4IN & SDA){
        i2c_status |= NAK_FLAG;
    }
    i2c_clock_cycle();
    for(j=I2C_DELAY; j!=0; j--){}
    P4DIR |= SDA; // SDA output port
}

void i2c_tx(char byte){
    for(i=8;i!=0;i--){
        if(byte & 0x80){
            i2c_tx_high_bit();
        }else{
            i2c_tx_low_bit();
        }
        byte = byte << 1;
    }
    i2c_read_ack();
}

void i2c_tx_address(char addr, char mode){
    i2c_start();
    addr = (addr << 1) + mode;
    i2c_tx(addr);
}

char i2c_rx(void){
    char data_in = 0x00;
    P4DIR &= ~SDA; // SDA input port
    for(j=I2C_DELAY*3; j!=0; j--){}

    for(i=8;i!=0;i--){
        if(P4IN & SDA){
            data_in = data_in + 0x01;
        }
        data_in = data_in << 1;
        i2c_clock_cycle();
    }
    for(j=I2C_DELAY; j!=0; j--){}
    P4DIR |= SDA; // SDA output port
    return data_in;
}

/**
 * main.c
 */
int main(void)
{
	WDTCTL = WDTPW | WDTHOLD;	// stop watchdog timer
	
	//------------------Configure I/O ports-----------------
    P4DIR |= SCL; // SCL output port
    P4DIR |= SDA; // SDA output port

    P4OUT |= SCL; //Set SCL high as default
    P4OUT |= SDA; //Set SDA high ad default

    PM5CTL0 &= ~LOCKLPM5; // Turn on GPIO

    while(1){
            i2c_tx_address(INT_TEMP_ADDR, WRITE_MODE);
            i2c_tx(0x0B);
            i2c_tx_address(INT_TEMP_ADDR, READ_MODE);
            int_temp = i2c_rx();
            i2c_nack();
            i2c_stop();
            for(i=0; i<254; i++){}

    }

	return 0;
}
