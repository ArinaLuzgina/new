
/*
 * rosserial Service Server
 */

#include <ros.h>
#include <ws_turtlebro_package/WayLan_Choice.h>
#include <std_msgs/UInt16.h>
#include <FastLED.h>

class NewHardware : public ArduinoHardware
{
  public:
  NewHardware():ArduinoHardware(&Serial1, 115200){};
};
ros::NodeHandle_<NewHardware>  nh;


#define WAY 25
#define LAN 22
#define NUM_LEDS 24 
#define DATA_PIN 30
CRGB leds[NUM_LEDS];

int way_led[] = {26, 27};
int lan_led[] = {28, 29};
int Way = 1;
char Lan = 'R';
bool before_way = 0;
bool before_lan = 0;
bool now_way = 0;
bool now_lan = 0;
using ws_turtlebro_package::WayLan_Choice;
void callback(const WayLan_Choice::Request & req, WayLan_Choice::Response & res){

  res.way = Way;
  if(Lan == 'E'){res.lan = "E";} else if(Lan == 'R'){res.lan = "R";}
}

ros::ServiceServer<WayLan_Choice::Request, WayLan_Choice::Response> server("button_srv",&callback);



void lamps(const std_msgs::UInt16& msg) {
    static uint8_t hue = 0; 
    int color = msg.data;
    if(color == 1){hue = 0;}else if(color == 2){hue = 64;}else if(color == 3){hue = 96;}
  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(hue, 255, 255);
    FastLED.show(); 
    fadeall();
    delay(20);
  }
}

void fadeall() { for(int i = 0; i < NUM_LEDS; i++) { leds[i].nscale8(250); } }

ros::Subscriber<std_msgs::UInt16> sub("led_color", lamps );

void setup()
{ 
  nh.initNode();
  nh.advertiseService(server);
  nh.subscribe(sub);
  
  pinMode(WAY, INPUT);
  pinMode(LAN, INPUT);
  before_way = digitalRead(WAY);
  before_lan = digitalRead(LAN);
  now_way = digitalRead(WAY);
  now_lan = digitalRead(LAN);
  if(now_way){Way = 1;} else {Way = 2;}
  if(now_lan){Lan = 'R';}else{Lan = 'E';}
  for(int i = 0; i < 2; i ++){pinMode(way_led[i], OUTPUT);
                              pinMode(lan_led[i], OUTPUT);}
  if(Way == 1){digitalWrite(way_led[0], HIGH);digitalWrite(way_led[1], LOW);}
  else if(Way == 2){digitalWrite(way_led[1], HIGH);digitalWrite(way_led[0], LOW);}
  if(Lan == 'R'){digitalWrite(lan_led[0], HIGH); digitalWrite(lan_led[1], LOW);}
  else if(Lan == 'E'){digitalWrite(lan_led[1], HIGH); digitalWrite(lan_led[0], LOW);}
  
  LEDS.addLeds<WS2812,DATA_PIN,RGB>(leds,NUM_LEDS);
  LEDS.setBrightness(60);
  int hue = 0;
  for(int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(hue, 255, 255);
    FastLED.show(); 
    fadeall();
    delay(20);
  }
}

void loop()
{ now_way = digitalRead(WAY);
  now_lan = digitalRead(LAN);
  if(before_way != now_way){before_way = now_way; if(Way==1){Way = 2; digitalWrite(way_led[1], HIGH);digitalWrite(way_led[0], LOW);}
                                              else if(Way == 2){Way = 1;digitalWrite(way_led[0], HIGH);digitalWrite(way_led[1], LOW);}}
  if(before_lan != now_lan){before_lan = now_lan; if(Lan=='R'){Lan='E';digitalWrite(lan_led[1], HIGH); digitalWrite(lan_led[0], LOW);}
                                            else if(Lan == 'E'){Lan = 'R';digitalWrite(lan_led[0], HIGH); digitalWrite(lan_led[1], LOW);}}

  
  
  nh.spinOnce();
  delay(1);
}
