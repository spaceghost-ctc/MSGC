// Feather LoRa Receiver Code
// MSGC BOREALIS

//Used for the LoRa 900 MHz Radio Feather M0 being used as a receiver. 
//Make sure to plug the uFl cable into an antenna and the usb port into a computer to save data.
#include <SPI.h>
#include <Wire.h>
#include <RH_RF95.h>
#include <Adafruit_SSD1306.h>
#define PACKET_LEN 0x79
#define RFM95_CS 8
#define RFM95_RST 4
#define RFM95_INT 3
#define RF95_FREQ 960.0
#define RF95_TXPOWER 23
#define RF95_SPREADINGFACTOR 10
#define RF95_SIGNALBW 500000 //doesn't do anything
#define THISADDRESS 0xFE
#define ACCEPTEDADDRESS 0xFD
#define LED 13
#define BUTTON_A  9
#define BUTTON_B  6
#define BUTTON_C  5

RH_RF95 rf95(RFM95_CS, RFM95_INT); // Singleton instance of the radio driver
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);
int displayMode = 0;        ///< Screen display mode(0=RSSI,TSLF,SNR,BoardID,Buffer; 1=Buffer; 2=GPS Data)
int timeOfLastSignal = 0;   ///< Helps to indicate how long ago the last transmission was
uint32_t timer = millis();  ///< Keeps track of when to refresh screen

// for message from radio
uint8_t buf[RH_RF95_MAX_MESSAGE_LEN];
uint8_t len = sizeof(buf);

// 256 Byte Receive Packet
uint8_t message[256];
  
void setup(){
  pinMode(LED, OUTPUT);
  pinMode(RFM95_RST, OUTPUT);
  digitalWrite(RFM95_RST, HIGH);
  Serial.begin(9600);
  while (!Serial) {delay(1);}
  delay(100);
  Serial.print("NIGEL|");
  Serial.println(len);
  //--Radio Setup--//
  digitalWrite(RFM95_RST, LOW);
  delay(10);
  digitalWrite(RFM95_RST, HIGH);
  delay(10);
  while (!rf95.init()) {while (1);}
  if (!rf95.setFrequency(RF95_FREQ)) {while (1);}
  rf95.setSpreadingFactor(RF95_SPREADINGFACTOR); //sets spreading factor
  rf95.setTxPower(RF95_TXPOWER, false);
  rf95.setPromiscuous(false);
  rf95.setThisAddress(THISADDRESS); //sets unique address for radio so it doesn't get unintended data
  rf95.setHeaderTo(ACCEPTEDADDRESS);
  rf95.setHeaderFrom(THISADDRESS);
  //--OLED Setup--//
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Address 0x3C for 128x32
  display.display();
  delay(1000);
  display.clearDisplay();
  display.display();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,0);
  pinMode(BUTTON_A, INPUT_PULLUP);
  pinMode(BUTTON_B, INPUT_PULLUP);
  pinMode(BUTTON_C, INPUT_PULLUP);
}

void loop(){
  unsigned int i;
  //--Radio Loop--//--receive message
  if (rf95.available()){
    if (rf95.recv(buf, &len)){
      if (rf95.headerFrom() == ACCEPTEDADDRESS) {
        digitalWrite(LED, HIGH);
        if((char)buf[0] == '['){
          Serial.print('['); //start character repeat
          for(i=0;i<len;i++){
            Serial.print(buf[i]);
            Serial.print(',');
          }
          Serial.print("RSSI");
          Serial.print(rf95.lastRssi(), DEC);
          Serial.print(',');
          Serial.print("SNR");
          Serial.print(rf95.lastSNR(), DEC);
          Serial.print(']');
          Serial.println("");
        }
        else if((char)buf[0] == '{'){
          Serial.print('{'); //start character
          for(i=0;i<len;i++){
            Serial.print(buf[i]);
            Serial.print(','); 
          }
          Serial.print("RSSI");
          Serial.print(rf95.lastRssi(), DEC);
          Serial.print(',');
          Serial.print("SNR");
          Serial.print(rf95.lastSNR(), DEC);
          Serial.print('}');
          Serial.println("");
        }
        else if((char)buf[0] == '('){
          Serial.print('('); //start character
          for(i=0;i<len;i++){
            Serial.print(buf[i]);
            Serial.print(','); 
          }
          Serial.print("RSSI");
          Serial.print(rf95.lastRssi(), DEC);
          Serial.print(',');
          Serial.print("SNR");
          Serial.print(rf95.lastSNR(), DEC);
          Serial.print(')');
          Serial.println("");
        }
        digitalWrite(LED, LOW);
        timeOfLastSignal = millis();
      }
      else{}
    }
  }
  //--END Radio Loop--//
  //--OLED Display Loop--//
  if(!digitalRead(BUTTON_A)) {
    displayMode = 0;
    updateScreen();
  }
  if(!digitalRead(BUTTON_B)) {
    displayMode = 1;
    updateScreen();
  }
  if(!digitalRead(BUTTON_C)) {
    displayMode = 2;
    updateScreen();
  }
  if (timer > millis()) timer = millis();
  if (millis() - timer > 2000){
    timer = millis();
    updateScreen();
  }
  //--END OLED DisplayLoop--//
}

void updateScreen() {
  display.clearDisplay();
  display.setCursor(0,0);
  switch(displayMode) {
    case 0:
    updateScreen0(); break;
    case 1:
    updateScreen1(); break;
    case 2:
    updateScreen2(); break;
    default: break;//Serial.println("You messed up your display modes somehow");
  }
  display.display();
}

void updateScreen0() {
  int i;
  display.print("RSSI:");
  display.print(rf95.lastRssi(), DEC);
  display.println(" TSLF:" + (String)((millis()-timeOfLastSignal)/1000));
  display.print("SNR:");
  display.println(rf95.lastSNR());
  display.println("NIGEL");
  display.print("Buffer:");
  display.print((char*)buf);    

}

void updateScreen1() {
  int i;
  display.print("Data Buf:");
        for(i=0;i<20;i++){
          display.print((char*)buf[i]);
          display.print(',');
        }
  display.println("");
  display.println("");
  }
  
void updateScreen2() {
  int i;
  display.print("GPS Data:");
        for(i=20;i<len;i++){
          display.print((char)buf[i]);
        }
  }
