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
Servo myServo; //new  servo objet


/*~~~~~~~~~~~~~~~~ Methods ~~~~~~~~~~~~~~~~*/
void pingLED(){
  float lightIntensity = analogRead(inPin);

  Serial.print(lightIntensity);
  Serial.print(',');
  Serial.print((millis() - startT)/1000.0);
  Serial.print(',');
  Serial.println(0);
}

void getSteps() {
  int val;

  while(Serial.available() > 0) {
    val = Serial.parseInt();
    if (val != 0) {
      myServo.write(val);
      Serial.print("> INITIATE MAGNET DESCENT ! ! ! AT T=");
      Serial.print((millis() - startT + 1000)/1000.0); 
      Serial.print(',');
      Serial.println(0);
    }
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

  // Servo //
  myServo.attach(servoPin);
  myServo.write(180);
  delay(5);
  // myServo.write(180);
  // delay(5);

  // Serial //
  Serial.begin(115200);
}




void loop() {

  getSteps();
  pingLED();
  delay(5);
}
