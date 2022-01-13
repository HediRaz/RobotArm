# RobotArm
Smart robot arm

This library allows you to controll a robotic arm usin your own hand or your own arm.


# Architecture
ServoFromPC.ino is the file that updates the arm position

comm.py gives some usefull functions to communicate with the Arduino from your PC

servo.py define the RobotArm class wich defines some rules for the arm

emulation.py define the class Emulation that is usefull to test your code before actually test it on the arm

# Projects
## Hand Tracking
Control the arm with only one hand.

## Arm Tracking
Control the arm like it is your arm.



