#include <Servo.h>

bool initialised = false;

const int nbServo = 6;  // nb of servo
Servo myServo[nbServo];
byte servoPin[nbServo] = {3, 5, 6, 9, 10, 11};  // servo pin
int servoMinPos[nbServo] = {-360, -360, -360, -360, -360, -360};  // min angle
int servoMaxPos[nbServo] = {360, 360, 360, 360, 360, 360};  // max angle
int servoPos[nbServo] = {90, 90, 90, 90, 90, 45};  // current positions wanted


const byte buffSize = 30;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

int messageServoPos[nbServo];

unsigned long curMillis;  // time since setup


void getDataFromPC() {
  // receive data from PC and save it into inputBuffer
  if(Serial.available() > 0) {
    char current = Serial.read();

    if (current == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }

    if(readInProgress) {
      inputBuffer[bytesRecvd] = current;
      bytesRecvd++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (current == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

 
void parseData() {
  // One type of message is accepted : <newPos0,newPos1,newPos2...>

  char *strtokIndx;

  strtokIndx = strtok(inputBuffer, ",");
  messageServoPos[0] = atoi(strtokIndx);
  for (int i = 1; i < nbServo; i++)
  {
    strtokIndx = strtok(NULL, ",");
    messageServoPos[i] = atoi(strtokIndx);  // convert to int
  }
}


void replyToPC() {
  // if data have been received, reply to PC
  if (newDataFromPC) {
    newDataFromPC = false;
    Serial.print("<Msg: Positions updated>");
  }
}


void updatePosition() {
  // if message received, write the new position
  if (newDataFromPC) {
    for (int i = 0; i < nbServo; i++)
    {
      messageServoPos[i] = max(messageServoPos[i], servoMinPos[i]);
      messageServoPos[i] = min(messageServoPos[i], servoMaxPos[i]);
      myServo[i].write(messageServoPos[i]);

      // if (servoPos[i] != messageServoPos[i]) {
      //   servoPos[i] = messageServoPos[i];
      // }
    }
  }
}


void setup() {
  Serial.begin(9600);
  
    // initialize the servo
  for (int i = 0; i < nbServo; i++){
    myServo[i].attach(servoPin[i]);
    myServo[i].write(servoPos[i]);
  }
  
    // tell the PC we are ready
  Serial.println("<Arduino is ready>");
}

void setup2() {
  for (int i = 0; i < nbServo; i++){
    myServo[i].write(servoPos[i]);
  }
  initialised = true;
}


void loop() {
  if (not initialised) {
    setup2();
  }
  curMillis = millis();
  getDataFromPC();
  updatePosition();
  replyToPC();
}
