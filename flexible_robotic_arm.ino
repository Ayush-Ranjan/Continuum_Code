#include <Servo.h>

// Define servo pins
const int innerHorizontalServoPin = 5;
const int outerHorizontalServoPin = 7;
const int innerVerticalServoPin = 8;
const int outerVerticalServoPin = 9;

// Create servo objects
Servo innerHorizontalServo;
Servo outerHorizontalServo;
Servo innerVerticalServo;
Servo outerVerticalServo;

// Current angles of the servos
int innerHorizontalAngle = 90;
int outerHorizontalAngle = 90;
int innerVerticalAngle = 90;
int outerVerticalAngle = 90;

void setup() {
  Serial.begin(9600);
  
  innerHorizontalServo.attach(innerHorizontalServoPin);
  outerHorizontalServo.attach(outerHorizontalServoPin);
  innerVerticalServo.attach(innerVerticalServoPin);
  outerVerticalServo.attach(outerVerticalServoPin);
  
  // Initialize servos to starting positions
  updateServoPositions();
  
  Serial.println("Servos initialized. Ready for commands.");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    processCommand(input);
  }
}

void processCommand(String input) {
  char servo = input.charAt(0);
  int angle = input.substring(1).toInt();
  
  switch(servo) {
    case 'I': // Inner Horizontal
      innerHorizontalAngle = constrain(angle, 0, 180);
      outerHorizontalAngle = constrain(outerHorizontalAngle + (angle - innerHorizontalAngle), 0, 180);
      break;
    case 'O': // Outer Horizontal
      outerHorizontalAngle = constrain(angle, 0, 180);
      break;
    case 'V': // Inner Vertical
      innerVerticalAngle = constrain(angle, 0, 180);
      outerVerticalAngle = constrain(outerVerticalAngle + (angle - innerVerticalAngle), 0, 180);
      break;
    case 'W': // Outer Vertical
      outerVerticalAngle = constrain(angle, 0, 180);
      break;
  }
  
  updateServoPositions();
  sendPositionFeedback();
}

void updateServoPositions() {
  innerHorizontalServo.write(innerHorizontalAngle);
  outerHorizontalServo.write(outerHorizontalAngle);
  innerVerticalServo.write(innerVerticalAngle);
  outerVerticalServo.write(outerVerticalAngle);
}

void sendPositionFeedback() {
  Serial.print(innerHorizontalAngle);
  Serial.print(",");
  Serial.print(outerHorizontalAngle);
  Serial.print(",");
  Serial.print(innerVerticalAngle);
  Serial.print(",");
  Serial.println(outerVerticalAngle);
}