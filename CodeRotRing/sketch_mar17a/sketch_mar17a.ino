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
float startT = millis();
Servo myServo;  //new  servo objet
bool go = false;


/*~~~~~~~~~~~~~~~~ Methods ~~~~~~~~~~~~~~~~*/
float pingLED() {
  float lightIntensity = analogRead(inPin);
  return lightIntensity;

  // Serial.println(550);
}

void getSteps() {
  int val;

  if (Serial.available() > 0) {
    val = Serial.read();
    if (val != 0) {
      myServo.write(val);
      //Serial.print("> INITIATE MAGNET DESCENT ! ! ! AT T=");
      //Serial.print(val);
      startT = millis();
      go = true;
    }
    Serial.flush();
  }
}

/*~~~~~~~~~~~~~~~~ RUN ~~~~~~~~~~~~~~~~*/
void setup() {
  // Pins //
  pinMode(inPin, INPUT);
  pinMode(LEDvoltPin, OUTPUT);
  digitalWrite(LEDvoltPin, HIGH);
  pinMode(photoVoltPin, OUTPUT);
  digitalWrite(photoVoltPin, HIGH);

  Serial.flush();
  // Servo //
  myServo.attach(servoPin);

  // Serial //
  Serial.begin(9600);
  

  myServo.write(180);
  delay(5);

}




void loop() {

  getSteps();

  if (go) {
    float lightIntensity = pingLED();

    Serial.print(lightIntensity);
    Serial.print(',');
    Serial.println((millis() - startT));

  }

}
