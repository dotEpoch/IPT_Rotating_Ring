int inPin = A0;
int voltPin = 5;


void setup() {
  // put your setup code here, to run once:
  pinMode(inPin, INPUT);
  pinMode(voltPin, OUTPUT);

  digitalWrite(voltPin, HIGH);

  Serial.begin(115200);
}

float startT = millis();
void loop() {
  // put your main code here, to run repeatedly:


  float lightIntensity = analogRead(inPin);
  Serial.print(lightIntensity);
  Serial.print(',');
  Serial.print(millis() - startT);
  Serial.print(',');
  Serial.print(0);
  Serial.println();
  delay(10);
}
