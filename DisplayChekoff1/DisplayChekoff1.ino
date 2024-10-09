#define HX8357X HX8357D
#define HX8357X_SPEED_MHX 20


#include <HX8357_t4x_p.h>
#include <Teensy_Parallel_GFX.h>

#define ROTATION 1

#define KURTS_MICROMOD

#include "SPI.h"

uint8_t use_dma = 0;
uint8_t use_clip_rect = 0;
uint8_t use_set_origin = 0;
uint8_t use_fb = 0;
uint8_t *tft_frame_buffer = nullptr;

#define ORIGIN_TEST_X 50
#define ORIGIN_TEST_Y 50

HX8357_t4x_p tft = HX8357_t4x_p(10, 8, 9);  //(dc, cs, rst)

#include <stdint.h>
#include "TouchScreen.h"

#define YM 24   // can be a digital pin
#define XM A11  // must be an analog pin, use "An" notation!
#define YP A12  // must be an analog pin, use "An" notation!
#define XP 27   // can be a digital pin

// For better pressure precision, we need to know the resistance
// between X+ and X- Use any multimeter to read it
// For the one we're using, its 300 ohms across the X plate
TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);


void setup() {
    while (!Serial && (millis() < 4000));

    Serial.begin(115200);

    if (CrashReport) {
        Serial.print(CrashReport);
        WaitForUserInput();
    }
    Serial.println("\n*** Sketch Startup ***");

#ifdef TFT_TOUCH_CS
    pinMode(TFT_TOUCH_CS, OUTPUT);
    digitalWrite(TFT_TOUCH_CS, HIGH);
#endif

    Serial.print("Teensy4.1 - ");
    tft_frame_buffer = (uint8_t *)extmem_malloc(tft.width() * tft.height() * 2 + 32);
    Serial.println(HX8357X_SPEED_MHX);
    tft.begin(HX8357X, HX8357X_SPEED_MHX);

    tft.setBitDepth(24);

    tft.displayInfo();

    // Frame buffer will not fit work with malloc see if
    if (tft_frame_buffer) tft.setFrameBuffer((uint16_t *)(((uintptr_t)tft_frame_buffer + 32) & ~((uintptr_t)(31))));


    //Set the current screen rotation and set default black.
    tft.setRotation(ROTATION);
    tft.fillScreen(HX8357_BLACK);
    Serial.printf("Screen width:%u height:%u\n", tft.width(), tft.height());

    //Make a touchreen page and serial print to verify each step works
    tft.fillScreen(HX8357_RED);
    tft.fillRect(tft.width()/5 * 2, tft.height()/5 * 2, tft.width()/5, tft.height()/5, HX8357_PINK);
    Serial.printf("One");
    tft.setTextColor(HX8357_WHITE);
    Serial.printf("Two");
    tft.setTextSize(2);
    Serial.printf("Three");
    tft.setCursor(tft.width()/2,tft.height()/2,true);
    Serial.printf("Four");
    tft.println(F("Press!"));
    Serial.printf("Five");
    

}
//Function that waits for enter press 
void WaitForUserInput() {
    Serial.println("Hit Enter to continue");
    Serial.flush();
    while (Serial.read() == -1)
        ;
    while (Serial.read() != -1)
        ;
}

//Used variables in game loop
int minx = 1000;
int maxx = 0;
int miny = 1000;
int maxy = 0;
bool pressed = false;

//Simulated arry from p
char occ1[4][4] = {{'b', 'b', 'b', 'b',}, {'b', 'b', 'b', 'b',}, {'b', 'b', 'b', 'b',}, {'r', 'b', 'b', 'b',}};
int count = 1;

void loop() {
  //Loop for game running after touch
  if(pressed){
    tft.fillScreen(HX8357_BLACK);
    for(int i = 0; i < 4; i++){
      for(int j = 0; j < 4; j++){
        int xVal = i * (tft.height()/4) + (tft.width() - tft.height())/2;
        int yVal = j * (tft.height()/4);
        tft.drawRect(xVal, yVal, tft.height()/4, tft.height()/4, HX8357_BLUE);
      }
    }
    for(int i = 0; i < 4; i++){
      for(int j = 0; j < 4; j++){
        int xVal = i * (tft.height()/4) + (tft.width() - tft.height())/2;
        int yVal = j * (tft.height()/4);
        if(occ1[i][j] == 'r'){
          tft.fillRect(xVal, yVal, tft.height()/4, tft.height()/4, HX8357_RED);
        }
      }
    }
    if(count == 1){
      Serial.println("1");
      occ1[3][0] = 'b';
      occ1[3][1] = 'r';
    }
    if(count == 2){
      Serial.println("2");
      occ1[3][1] = 'b';
      occ1[3][2] = 'r';
    }
    if(count == 3){
      Serial.println("3");
      occ1[3][2] = 'b';
      occ1[3][3] = 'r';
    }
    count++;
  }

  delay(1000);
  TSPoint p = ts.getPoint();
  
  //Statement to test X and Y ranges to calibrate
  // if (p.z > ts.pressureThreshhold) {
  //   if (p.x < minx)
  //     minx = p.x;
  //   if (p.x > maxx)
  //     maxx = p.x;
  //   if (p.y < miny)
  //     miny = p.y;
  //   if (p.y > maxy)
  //     maxy = p.y;
  //   Serial.print("Range x: "); Serial.print(minx); Serial.print(" "); Serial.println(maxx);
  //   Serial.print("Range y: "); Serial.print(miny); Serial.print(" "); Serial.println(maxy);
  // }

  //pressure of 0 means no pressing!
  //Decoding coordinates into 0-100 values
  if (p.z > ts.pressureThreshhold) {
    p.x = (p.x - 124) * (100) / (903 - 124); 
    Serial.print("X = "); Serial.print(p.x);
    p.y = (p.y - 70) * (100) / (926 - 70);
    Serial.print("\tY = "); Serial.print(p.y);
    Serial.print("\tPressure = "); Serial.println(p.z);
  }

  //If pressed within box start game
  if(p.x > 45 && p.x < 55 && p.y > 45 && p.y < 55){
    pressed = true;
  }
  

  delay(100);
}
