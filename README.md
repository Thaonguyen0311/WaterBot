
Watering robot - Waterbot
Jump to navigationJump to search
Participant	Supervisor
Josuar Priebe	Prof. Dr.-Ing. Andreas Maier
Nick Heidenfelder	Prof. Dr. Thomas Fuhrmann
Thao Nguyen
Wolf Hausdorf

Waterbot in the greenhouse of the Botanical Garden of the University of Regensburg

Table of contents
1	Project description
2	Hardware
2.1	Bill of materials
3	chassis
3.1	mechanics
4	Navigation and wayfinding
4.1	Circuit boards for locomotion and navigation
4.1.1	esp32 code
4.2	supply
5	Irrigation system
5.1	pump
5.2	Level sensor
5.3	servo motor
6	Plant recognition software
6.1	Raspberry Pi 5
7	Business plan
8	Challenges and Outlook
9	files
9.1	STL files:
9.2	Layout files:
9.3	Code:
9.4	Business plan:
Project description 
The goal of this project was to build an autonomous watering robot. For gardens, greenhouses, and homes with a large number of different plants, there is currently no convenient automated solution for watering plants. The robot follows a pre-laid wire without physical contact and identifies plants using a camera. A self-built level sensor protects the submersible pump from running dry. The pumped water jet is directed vertically by a servo motor. An ultrasonic sensor prevents the robot from hitting or driving over obstacles.

Hardware 
Bill of materials 
components	Number
Stepper motor PSM42BYGHW603, 1.8°	2
Stepper motor driver DAYCOM ST-A4988	2
cylewet 100 IR infrared distance sensor	9
GRV HUMIDITY SENSOR :: Arduino - Grove Humidity Sensor	1
Diaphragm valve CONJOIN CJV23-C12A1	1
ball rollers	1
Model building board	1
Poplar plywood	1
sponge	3
battery	1
Wheel?	2
5l tank	1
DC worm gear motor	2
Aluminum profile angle connector	1
Aluminum profile 30×30, 2000 mm (groove 8)	1
PLA filament 1 kg	1
Furniture swivel caster (DIY store)	1
Resistors (assortment / 10–50 pieces)	1
Timer IC NE555 (DIP or SOIC)	1
Microcontroller board ESP32 Dev board (ESP32-WROOM)	1
Operational amplifier OPA2365AIDR	2
Printed circuit board (PCB) (China, 2-layer, 5 pieces)	1
Transistor BC338-40	4
TS2940 Low Dropout Regulator (LDO)	1
MOSFET IRL3103PBF	1
Ultrasonic sensor HC-SR04	1
Chassis 
Mechanics 
The Waterbot's basic frame is made from 30x30mm extruded aluminum profile. Two independently controllable DC motors are mounted at the front, with a freewheel roller in the center at the rear. A 5L canister is attached in the center. The individual electronic components are mounted in 3D-printed housings along a vertical aluminum profile column. The column terminates with a bracket for the servo motor and the attached spray head.


Chassis design made of aluminum profiles and angles
To secure the electronic components, such as circuit boards and batteries, as well as the housing and wheels, specially adapted 3D-printed brackets and components were manufactured. These were then securely mounted to the chassis using M6 screws in combination with T-nuts. The covers of the 3D-printed housings were attached with M3 screws, ensuring easy access at all times. Each wheel was fixed to the axle using two 10 mm long M3 screws.


3D prints
Navigation and wayfinding 
To ensure reliable pathfinding, the system follows the magnetic field of a conductor that marks the path. A square wave generator with a power stage is used to generate this magnetic field, maximizing the current change. Two coils, each with two signal paths to the microcontroller, are used to detect the field. Within these paths, the signal is amplified and converted into a DC voltage level. This is achieved by charging a capacitor with the rising edge of the signal, which is then discharged in a controlled manner via a potentiometer. At the end of the signal path, the capacitor is protected from discharge by an impedance converter. Finally, an LED is connected for easy calibration.


Circuit diagram of signal paths to the microcontroller

Circuit diagram NE555 square wave generator with power stage

Demonstration image: Test drive to track the line
Circuit boards for locomotion and navigation 
A mainboard was developed for the chassis, serving as the central interface between the ESP32 and the peripherals. The board comprises the following functional groups:

Signal processing: Integrated level shifters for level adjustment for controlling the motor drivers and the ultrasonic sensor.

Power supply: DC-DC converters that efficiently transform the 12V battery voltage into the required system voltages of 5V and 3V.

Communication & Interface: Lines for data exchange with the ESP32 and status LEDs for visual system control.

Expandability: Generous perforated grid panels for future hardware upgrades or additional modules.


Circuit board layout of the landing gear main board

The signal generator board generates the magnetic field around the conductor through a combination of an astable multivibrator and a power stage. An NE555 timer first generates a precise 12V square wave signal, which serves as the control input for a high-power N-channel MOSFET. This MOSFET acts as an electronic switch, switching the full operating voltage onto the induction loop in sync with the signal. To protect the components and the power source from overload, power resistors are integrated into the circuit, reliably limiting the maximum current flow and thus ensuring a stable field for the sensors.


Circuit board layout of the signal generator board
esp32 Code 
Code: The ESP32 acts as a slave and receives start and stop signals from the Raspberry Pi. During driving (start state), the main loop uses the difference between the two sensor values ​​to determine whether the vehicle will drive straight ahead or turn left or right. If an obstacle is detected or the Raspberry Pi sends a stop signal, this loop is interrupted.


Status diagram created with plantuml.com
The ESP32RobotMain class handles the central coordination of the hardware components. Data processing takes place in the SensorSignalProcessor, which filters the noise of the analog values ​​by averaging ten times and provides the distance data from the ultrasound sensors. These filtered values ​​are used by the navigation system logic to calculate the difference between the left and right sensors and derive corresponding steering commands. These commands are then transmitted to the DriveTrain for PWM control of the motors and to the user interface for visual status display via the RGB LED.


UML diagram created with plantuml.com
Supply 
The entire robot is powered by a 3S lithium-ion battery, which delivers 9.7–12.6V. This voltage level is used for the submersible pump, the servo, and the DC motors for propulsion. For the Raspberry Pi 5, the battery voltage is regulated down to 5V via a switching regulator. A 3.3V LDO supplies power to the ESP32.

Irrigation system 
Pump 
The pump is switched using an N-channel MOSFET as a low-side switch in the pump's ground path. The selected MOSFET has such a low breakdown voltage that the gate can be switched directly via the Raspberry Pi's GPIO pin. This circuit was implemented on a perforated circuit board and protected from environmental influences with heat-shrink tubing.


Circuit diagram pump driver
Level sensor 
The custom-designed level sensor uses NPN bipolar transistors and the conductivity of the water. When a base is connected to the sensor's lead via the water, the transistor switches, and the change in state can be measured at the Raspberry Pi's GPIOs, which are connected to the respective collectors of the transistors. Using such circuits at different heights in the canister, the fill level can be displayed from 0-100% in 25% increments.


Circuit diagram for the level sensor
Servo motor 
The servo motor is controlled directly via a GPIO of the Pi.


Pinout for the Raspberry Pi 5
Plant recognition software 
Raspberry Pi 5
Auf dem Raspberry Pi laufen zwei Programme parallel, zum einen die Software für die Füllstanderkennung und zum anderen die Pflanzenerkennung mit dem Ablauf für die für das Stoppen des Waterbots und das Giesen der Pflanzen. Die Füllstanderkennung liest die Sensoreingänge aus und schaltet je nach Füllstand vier LEDS zur optischen Darstellung des Füllstands, bei Füllstand 0% wird über einen GPIO des Pi ein Buzzer angesteuert um ein akustisches Signal für leeres Wasser zu geben. Außerdem wird ein Taster ausgelesen mit dem die LEDs abgeschaltet werden könnnen um Energie zu sparen.


LED Anzeige für den Füllstand
Die Pflanzen Erkennung wird mitels YOLOE Computervision umgesetzt. Hier wird ein vortrainiertes Model mit Bildern oder Text gepromptet. Aufgrund der vergleichsweise schwachen Rechenleistung des Raspberry pi für solche Anwendungen konnten einzelne Pflanzen nicht schnell genug unterschieden werden. Als Kompromiss wurde auf vergleichsweise einfache Symbole in verschiedenen Farben zurückgegriffen. Bei 10 verschiedenen Symbolen und 7 verschiedenen Symbol- und Hintergrundfarben, können immerhin 210 Kombinationen erreicht werden.

Der Programmablauf zu aller erst die CSV mit den Pflanzendaten geladen und startet das CV Modell um nach Pflanzen zu suchen. Dann ein Start Signal zum ESP32 geschickt, so dass waterbot los fahren kann. Wenn eine Pflanze bzw. ein Symbol im mittleren fünftel der Kameraaufnahme erkannt wird, wird ein Stoppsignal an den ESP32 geschickt und in den Pflanzendaten nach dieser Pflanze gesucht und ausgerechnet ob die letzte Gieszeit addiert mit dem Giesintervall kleiner als die aktuelle zeit ist. Zur einfachen Rechnung wird hier Unixzeit verwendet. Falls das Giesintervall noch nicht überschritten wurde, wird nach der nächsten pflanze gesucht, dieser check ist so schnell, dass die Motoren in einem solchen fall nicht ganz zum stillstand kommen, diese Trägheit des Systems wird ausgenutzt um ein ständiges Stop-and-Go des Waterbot zu vermeiden. Im Falle, dass das Giesinterval überschritten wurde, bleibt Waterbot stehen, über die y-Position im Bild der Kamera wird der dutycycle für den Servomotor ausgerechnet und dann der Servo mit diesem Dutycycle angesteuert. Die Pumpe wird für die Anzahl der Sekunden die in den Pflanzendaten spezifiziert ist angesteuert und dann wieder abgestellt. Die neue Gieszeit wird in den Pflanzendaten hinterlegt und in einer CSV Datei gespeichert. Ein Start Signal wird wieder an den ESP32 geschickt und der loop startet von vorne.


Symbolerkennung in Aktion
Businessplan

Logo
The business plan fully summarizes Waterbot as both a product and a business venture. It describes the problem Waterbot aims to solve and the potential benefits the robot offers to private and commercial users. Building on this foundation, target groups, market potential, and existing solutions are analyzed to clearly define the planned positioning and differentiation. Furthermore, the plan outlines how market entry, marketing, and sales would need to be implemented, and how production and organizational structures could be established. In addition to the current product generation, the plan also sketches the company's potential future development, including planned expansions such as additional models and an outlook for the coming years. The plan concludes with a financial plan detailing pricing logic, revenue and cost assumptions, capital requirements, and the most important planning parameters.











Challenges and Outlook 
Aiming via the servo motor requires manual recalibration depending on the camera's position. Mechanically connecting the camera to the servo and using a rangefinder or distance estimator could resolve this issue. Recognizing different plants is too slow on the Pi; this could be improved with a graphics card or the AI ​​HAT for Raspberry Pi. A graphical user interface would significantly simplify the process of learning new plants or symbols.


Waterbot in action
Files 
STL files: 
File: 3D Printer STL files.zip

Layout files: 
File:Gerber wasserRobo2 PCB 2026-02-03.zip

File: Gerber wasserRobo PCB 026-02-03.zip

File:BOM wasserRobo 2026-02-03.zip

File:BOM wasserRobo2 2026-02-03.zip

Code: 
File:ESP-32 Code water robo.zip

File:Waterbot rpi code.zip

Business plan: 
File:Waterbot Businessplan Final.pdf

Categories :VMS - Advanced Measurement and Sensor TechnologyProf. Dr.-Ing. Andreas MaierProf. Dr. Mikhail Chamonine
Navigation menu
Ngt33980
discussion
Settings
Watchlist
Posts
Log out
Pagediscussion
To readEditVersion historyObserve

More
Search
Search EI-Wiki
Main page
Recent changes
Random page
EI-Wiki Help
Quick links
Professors
Organizational/Useful Information
Occupational safety
Laboratories
Vacancies
Tools
Links to this page
Changes to linked pages
Upload file
Special pages
Print version
Permanent link
Page information
This page was last edited on 4 February 2026 at 20:50.
This page has been viewed 152 times.
Data protectionAbout EI-WikiDisclaimer
Powered by MediaWikiPowered by Debian
