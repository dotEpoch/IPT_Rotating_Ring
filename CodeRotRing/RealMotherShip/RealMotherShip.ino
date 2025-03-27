/*
--- Rotating Magnetic Ring Experimental Setup  ---
Authors: Vincent Aucoin, Didar Sedghi
Description: 
*/

// Packages //
#include <Servo.h>

// Initialization //
int inPin = A0;
int photoVoltPin = 4;
int LEDvoltPin = 2;
int servoPin = 9;
uint32_t startT;
Servo myServo;  //new  servo objet
bool go = false;


/*~~~~~~~~~~~~~~~~ Methods ~~~~~~~~~~~~~~~~*/
float pingLED() {
  float lightIntensity = analogRead(inPin);
  return lightIntensity;

  // Serial.println(550);
}

void getSteps() {
  int val = Serial.parseInt();
  myServo.write(val);
  //Serial.print("> INITIATE MAGNET DESCENT ! ! ! AT T=");
  //Serial.print(val);
  startT = millis();
  go = true;
}

/*~~~~~~~~~~~~~~~~ RUN ~~~~~~~~~~~~~~~~*/
void setup() {
  // Pins //
  pinMode(inPin, INPUT);
  pinMode(LEDvoltPin, OUTPUT);
  digitalWrite(LEDvoltPin, HIGH);
  pinMode(photoVoltPin, OUTPUT);
  digitalWrite(photoVoltPin, HIGH);

  
  // Servo //
  myServo.attach(servoPin);

  // Serial //
  Serial.begin(115200);
  

  myServo.write(180);
  delay(5);

}



uint32_t prev_time = startT;
uint32_t time;
void loop() {
time = millis() - startT;

  if (go && (time > prev_time)) {
    int lightIntensity = analogRead(inPin);
    prev_time = time;

    Serial.print(lightIntensity);
    Serial.print(',');
    Serial.println(time);
  }
  else if (Serial.available() > 0) {
    int val = Serial.parseInt();
    myServo.write(val);
    startT = millis();
    go = true;
  }
}
