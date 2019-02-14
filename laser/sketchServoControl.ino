/*
 * This sketch sets up the servo and Serial Connections and updates
 * the servo based on the input of the Serial Connection
 */
#include <Servo.h> //include teh Servo header for easier servo control

Servo myservo;//creates the servo object

int pos = 0;//used for changing the angle of the motor
int currentPos = 0; //used to keep track of where the motor is currently
int usrInt = 0;//used to keep track of the number the user inputted

void setup() { //this runs only once when it starts
  Serial.begin(9600);//start the serial connection at 9600 baudrate
  myservo.attach(12);//attach the servo to the pin 12
  myservo.write(0); //Resets the servo to 0 degrees

}

void loop() { //loops forever (with power after setup)
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0)//if there is a new command in the Serial
  {
    usrInt = Serial.parseInt();//take the information given as an int and set userInt equal to it
    Serial.parseInt(); //take it again to clear the Serial but do nothing with it
    delay(10); //wait 10 ms
  }


  if(usrInt >180)//if over 180 mod the input by 180 to make it in range
  {
    usrInt = usrInt%180;
  }
  else if(usrInt < 0)//else if under 180 mod the absolute value of the input by 180 to get it in range
  {
    usrInt = abs(usrInt)%180;
  }
  Serial.println(usrInt); //print the number the user inputted back to the user

  if(usrInt > currentPos)//if the input is bigger than the current angle
  {
    for(pos = currentPos; pos <= usrInt; pos += 1) {//starting at the currentPos number, as long as the pos (counter) is less than the input,
      myservo.write(pos);                           //write the servo to 1 more degrees than before until it reaches the input
      delay(10);//wait 10 ms
      currentPos += 1; //increment the currentPos counter
    }
  }

  if(usrInt < currentPos)//if the input is smaller than the current angle
  {
    for(pos = currentPos; pos >= usrInt; pos -= 1) {//starting at the currentPos number, as long as the pos (counter) is more than the input,
      myservo.write(pos);                           //write the servo to 1 less degrees than before until it reaches the input
      delay(10);//wait 10 ms
      currentPos -= 1;//decrement the currentPos counter
    }
  }
   
}
