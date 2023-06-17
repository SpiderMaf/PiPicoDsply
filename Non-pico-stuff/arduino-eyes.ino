/**************************************************************************
 This is an example for our Monochrome OLEDs based on SSD1306 drivers

 Pick one up today in the adafruit shop!
 ------> http://www.adafruit.com/category/63_98

 This example is for a 128x32 pixel display using I2C to communicate
 3 pins are required to interface (two I2C and one reset).

 Adafruit invests time and resources providing this open
 source code, please support Adafruit and open-source
 hardware by purchasing products from Adafruit!

 Written by Limor Fried/Ladyada for Adafruit Industries,
 with contributions from the open source community.
 BSD license, check license.txt for more information
 All text above, and the splash screen below must be
 included in any redistribution.
 -------
 Modified from the above library to add some code for a robot eyes effect
 on an ssd-1306 oled desplay.  All credit to the original authors and adafruit
 above - as I have no chance of writing the core ssd-1306 libraries myself
 
 **************************************************************************/



#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define EYE     12 
#define PUPIL     5 
#define TICK     1000 
#define EXR 35
#define EXL 95

#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16
static const unsigned char PROGMEM logo_bmp[] =
{ 0b00000000, 0b11000000,
  0b00000001, 0b11000000,
  0b00000001, 0b11000000,
  0b00000011, 0b11100000,
  0b11110011, 0b11100000,
  0b11111110, 0b11111000,
  0b01111110, 0b11111111,
  0b00110011, 0b10011111,
  0b00011111, 0b11111100,
  0b00001101, 0b01110000,
  0b00011011, 0b10100000,
  0b00111111, 0b11100000,
  0b00111111, 0b11110000,
  0b01111100, 0b11110000,
  0b01110000, 0b01110000,
  0b00000000, 0b00110000 };


void setup() {
  Serial.begin(9600);

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  //display.display();
  //delay(2000); // Pause for 2 seconds

  // Clear the buffer
  display.clearDisplay();

  // Draw a single pixel in white
  //display.drawPixel(10, 10, WHITE);

  // Show the display buffer on the screen. You MUST call display() after
  // drawing commands to make them visible on screen!
  display.display();
  //delay(2000);
  // display.display() is NOT necessary after every single drawing command,
  // unless that's what you want...rather, you can batch up a bunch of
  // drawing operations and then update the screen all at once by calling
  // display.display(). These examples demonstrate both approaches...

  //testdrawcircle();    // Draw circles (outlines)

  //testfillcircle();    // Draw circles (filled)


  // Invert and restore display, pausing in-between
  //display.invertDisplay(true);
  //delay(1000);
  //display.invertDisplay(false);
  //delay(1000);
int vpos = 18;
display.drawRect(10, 10, 118, 20, WHITE); 
display.display();
  for(int16_t i=1; i<114; i+=2) {
    display.fillRect(12, 12, i, 16, WHITE);  
    display.display();
    delay(2);
    }
delay(100);
    
}

void drawEyes(int plh,int prh,int plv,int vpos){
    display.clearDisplay();
    display.fillCircle(EXR, vpos, EYE, WHITE);
    display.fillCircle(EXL, vpos, EYE, WHITE);
    display.fillCircle(EXR+plh, vpos+plv, PUPIL, BLACK);
    display.fillCircle(EXL+prh, vpos+plv, PUPIL, BLACK);
  }

void displayTick(){
     display.display();
    delay(TICK);
}
void eyelid(int vpos){
    display.clearDisplay();
    display.drawCircle(EXR, vpos, EYE, WHITE);
    display.drawCircle(EXL, vpos, EYE, WHITE);  
    display.fillRect(0, 0, 132, 25, BLACK);  
    display.display();
    delay(150);
}

void centerDraw(int vpos){
  drawEyes(1,-1,0,vpos);
  }

void center(int vpos){
  centerDraw(vpos);
  displayTick();
  }

  void left(int vpos){
  drawEyes(-3,-3,0,vpos);
  displayTick();
  }

  void right(int vpos){
  drawEyes(3,3,0,vpos);
  displayTick();
  }

  void up(int vpos){
  drawEyes(1,-1,-3,vpos);
  displayTick();
  }
void down(int vpos){
  drawEyes(1,-1,3,vpos);
  displayTick();
  }

void lookLeft(int vpos){
  left(vpos);
  center(vpos);
  }

void lookRight(int vpos){
  right(vpos);
  center(vpos);
  }

void confuse(int vpos){
  drawEyes(4,-4,0,vpos);
  displayTick();
  }

void eyeblink(int vpos){
  centerDraw(vpos);
  for(int16_t i=0; i<30; i+=5) {
    display.fillRect(0, 0, 132, 10+i, BLACK);  
    display.display();
    delay(1);
    }
  }

void eyelidBlink(int vpos){
  center(vpos);
  eyelid(vpos);
  center(vpos);
  }

int vpos=18;
int timeRND=0;
int actionRND=0;

void loop() {
  timeRND=random(5);
  actionRND=random(20);
  delay(TICK*timeRND);
  eyelidBlink(vpos);
  center(vpos);
  switch (actionRND) {
  case 1:
  eyeblink(vpos);
      break;
  case 2:
  eyelidBlink(vpos);
      break;
  case 3:
  confuse(vpos);
      break;
  case 4:
  up(vpos);
      break;
  case 5:
  down(vpos);
      break;
  case 6:
  left(vpos);
      break;
  case 7:
  right(vpos);
      break;
  case 8:
  lookLeft(vpos);
      break;
  case 9:
  lookRight(vpos);
      break; 
  case 10:
  left(vpos);
  right(vpos);
  left(vpos);
  right(vpos);
  center(vpos);
      break;
    case 11:
  down(vpos-1);
  center(vpos);
      break;
      
    default:
    center(vpos);
    break;
  }
}  
