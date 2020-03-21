#include<SoftwareSerial.h>
// ORANGE = TX on Roomba
// YELLOW = RX on Roomba

#define OPCODE_START        128
#define OPCODE_SAFE         131
#define OPCODE_FULL         132
#define OPCODE_POWER        133
#define OPCODE_LEDS         139
#define OPCODE_DRIVE        137
#define OPCODE_DRIVE_DIRECT 145

#define BAUD_RATE 115200


/*
 * LED_bits: 0 - Debris | 1 - Spot | Dock - 2 | Check Robot - 3
 * Color: 0 - green | 255 - red
 * Intensity: 0 - off | 255 - full intensity
 */
void write_LED(const uint8_t& LED_bits, const uint8_t& color, const uint8_t& intensity) {
  uint8_t buf_len = 4;
  uint8_t* buf = new uint8_t[buf_len];
  buf[0] = OPCODE_LEDS;
  buf[1] = LED_bits;
  buf[2] = color;
  buf[3] = intensity;

  Serial.write(buf, buf_len);
  
}
void setup() {
  
  // init UART
  Serial.begin(BAUD_RATE);

  // wait 1 sec upon boot up to write startup
  delay(1000);

  // send OPCODE_START to enable UART control of roomba
  Serial.write(OPCODE_START);
  Serial.write(OPCODE_SAFE);
  write_LED(4,255,255);
}

void loop() {
  // put your main code here, to run repeatedly:

}
