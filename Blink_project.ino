
// Pin assignments
// Arduino pin numbers
const int SW_pin = 2; // digital pin connected to switch output
const int X_pin = 0; // analog pin connected to X output
const int Y_pin = 1; // analog pin connected to Y output


#define UP_LED 8
#define RIGHT_LED 9 
#define LEFT_LED 10
#define DOWN_LED 11






void setup() {
  pinMode(SW_pin, INPUT);
  digitalWrite(SW_pin, HIGH);
  Serial.begin(115200);


  pinMode(UP_LED , OUTPUT);
  pinMode(RIGHT_LED , OUTPUT);
  pinMode(LEFT_LED , OUTPUT);
  pinMode(DOWN_LED , OUTPUT);

}

void loop() {
  Serial.print("Switch:  ");
  Serial.print(digitalRead(SW_pin));
  Serial.print("\n");
  Serial.print("X-axis: ");
  Serial.print(analogRead(X_pin));
  Serial.print("\n");
  Serial.print("Y-axis: ");
  Serial.println(analogRead(Y_pin));
  Serial.print("\n\n");
  
  delay(20);


  if(analogRead(X_pin) == 1023){
    digitalWrite(UP_LED , HIGH);

 } else if(analogRead(X_pin) == 0){
    digitalWrite(DOWN_LED , HIGH);
}

else if(analogRead(Y_pin) == 1023){
    digitalWrite(RIGHT_LED , HIGH);
}

else if(analogRead(Y_pin) == 0){
    digitalWrite(LEFT_LED , HIGH);

}

else if(digitalRead(SW_pin) == 0){
digitalWrite(UP_LED , HIGH);
digitalWrite(LEFT_LED , HIGH);
digitalWrite(RIGHT_LED , HIGH);
digitalWrite(DOWN_LED , HIGH);


}





else{
digitalWrite(UP_LED , LOW);
digitalWrite(LEFT_LED , LOW);
digitalWrite(RIGHT_LED , LOW);
digitalWrite(DOWN_LED , LOW);

  
  
}
  }









  




