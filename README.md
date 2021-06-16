# Self-Parking-Car

The system is a low-cost prototype for implementing a parallel parking algorithm on a mobile robot car, using a Raspberry Pi, camera, Ultrasonic sensors and an optical sensor. A hardware push button starts process of self-parking the car. On pressing the button, the robot moves forward, while scanning for vacant spots on the side using ultrasonic sensor array and the camera. On finding a suitable spot of appropriate dimensions, the robot moves forward and stops at an appropriate distance. The robot then makes a 45 degree turn and back up into the spot. The ultrasonic sensors at the back of the robot allows it to move backward till the obstacle. Then the robot makes another 45 degree in the opposite direction to become straight. After this using the front and rear sensors, the robot can park itself within the spot. The control algorithm goes through various stages, where the Raspberry Pi would use various combinations of the sensor data to make decisions and rotate the servo motors in appropriate direction to maneuver the robot. The robot car should select only those spots in which it can fit in. It should also not collide with the walls or other vehicles during the entire process.

![Concept](https://github.com/vv258/Self-Parking-Car/blob/master/images/1.png)

## Software Design
The system software consists of the Self-Parking State Machine and associated functions and interfaces .  

**Self-Parking State Machine:** The FSM is used to move the Robot Car from initial position to the final parked position. The various states make use of different combinations of sensors to control the movement of the robot .  
![FSM1](https://github.com/vv258/Self-Parking-Car/blob/master/images/2.png)
![FSM2](https://github.com/vv258/Self-Parking-Car/blob/master/images/3.png)

**Hardware PWM generation:** The PWM signal required for controlling the servo motors is generated using the pigpio library. Pigpiod is a utility which launches the pigpio library as a daemon. Once launched the pigpio library runs in the background accepting commands from the pipe and socket interfaces. The pigpiod utility requires sudo privileges to launch the library but thereafter the pipe and socket commands may be issued by normal users .  

**Optical mouse odometry:** The position of the robot at any point of time is sensed using an optical mouse connected over USB port. The optical mouse, when being used on the computer for a graphical user interface, returns a dx (change in the x coordinate) and dy (change in y coordinate) to move the mouse pointer on the screen. These values can be integrated to obtain the real time x an y coordinates of the mouse. Hence, the mouse is attached with the robot. When the robot moves forward, the x coordinate of the mouse should remain constant to make sure it is running in a straight line. The y coordinate of the mouse would provide the distance travelled by the robot. The mouse movements in the x and y direction are accumulated using a background process. Any movement in mouse is captured and immediately updated on a FIFO. The main application reads from FIFO to get the current position .  

**Movement control:** To make the robot move in a straight line, the initial x and y positions are stored, the left motor is rotated in anticlockwise direction and right motor is rotated in clockwise direction. The right motor is moved at a constant speed and the speed of the left motor is varied in proportion to the difference between current x position and initial x position to minimize the error and maintain straight line movement until current y position matches the desired value. For rotating the robot, the motors are rotated in same direction and same speed. When the current x value matches desired value, the rotation is stopped .  

**Fire hydrant detection:** The image processing algorithm looks for red objects in the frame and if a red object of dimension larger than the set value is detected, it is tagged as a fire hydrant. The detection was carried out using OpenCV library. The frame from the camera is captured and converted from RGB to HSV color space. The image is masked to detect only red pixels. Further computation intensive processing is done only if number of pixels exceed the minimum threshold, otherwise the frame is discarded. The boundary and center of the object is then extracted. If the radius is higher than the minimum set value, the object is tagged as a fire hydrant .  

**Ultrasonic Interface:** The HC-SR04 distance measuring transducer can be easily interfaced with code. However, using readily available library makes it easier to add multiple sensors and avoid cluttering up the main program code. The Bluetin_Echo library was installed using PIP used to read the sensor in centimeter scale .  

**User Interface:** The user interface for the systems consists of a pushbutton and a PiTFT. The push button is sensed through interrupt processing using RPi.GPIO library. The Pygame library provides an excellent platform for implementing the GUI. The GUI provides feedback to the user about the current state of the parking algorithm and also forms a useful tool for debugging .  

More Details at: [Hackster.io](https://www.hackster.io/vipinvngpl1992/self-parking-car-4ded0d "Self Parking Car")
# Self-Parking-Car_Qi_update
