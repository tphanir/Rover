#include <Adafruit_PWMServoDriver.h>
#include <Wire.h>



String curr = "";

// Create an instance of the PCA9685 driver
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

const int MAX = 4095;

const int left_l = 6; 
const int left_r = 7; 

const int right_l = 8; 
const int right_r = 9; 


void setMotor(int rpwmChannel, int lpwmChannel, int speed) {
  if (speed > 0) {
    // Forward: RPWM = speed, LPWM = 0
    pwm.setPWM(rpwmChannel, 0, speed);
    pwm.setPWM(lpwmChannel, 0, 0);
  } else if (speed < 0) {
    // Reverse: RPWM = 0, LPWM = -speed
    pwm.setPWM(rpwmChannel, 0, 0);
    pwm.setPWM(lpwmChannel, 0, -speed);
  } else {
    // Stop: Both PWM channels = 0
    pwm.setPWM(rpwmChannel, 0, 0);
    pwm.setPWM(lpwmChannel, 0, 0);
  }
}


void command(String direction) {
  if(direction == "f") {
    setMotor(left_r, left_l, -MAX);
    setMotor(right_r, right_l, MAX);
  } else if (direction == "b") {
    setMotor(left_r, left_l, MAX);
    setMotor(right_r, right_l, -MAX);
  } else if (direction == "l") {
    setMotor(left_r, left_l, MAX);
    setMotor(right_r, right_l, MAX);
  } else if (direction == "r") {
    setMotor(left_r, left_l, -MAX);
    setMotor(right_r, right_l, -MAX);
  } else if (direction == "s") {
    setMotor(left_r, left_l, 0);
    setMotor(right_r, right_l, 0);
  }
}


void setup() {
  Serial.begin(115200);
  Serial.println("Initializing PCA9685...");

  pwm.begin();                
  pwm.setPWMFreq(1000); // Set frequency to 1 kHz
  
  Serial.println("Initialized");

}

void loop() {

  if (Serial.available() > 0) { // Check if data is available to read
    String instruction = Serial.readStringUntil('\n'); // Read input until newline
    instruction.trim(); // Remove any leading or trailing whitespace
    if(curr != instruction) {
      Serial.print(instruction);
      command(instruction);
      instruction = curr;
    }
  }
  //command("s");
  
}
