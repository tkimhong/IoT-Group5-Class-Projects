# IoT Lab 2: ESP32 Web-Based IoT Control System

This IoT project creates a comprehensive web-based control system using ESP32, DHT22 temperature/humidity sensor, HC-SR04 ultrasonic distance sensor, and I²C LCD display. The system provides real-time sensor monitoring, LED control, and LCD display management through a responsive web interface.

---

# Hardware Components

- ESP32 Dev Board (flashed with MicroPython firmware)
- DHT22 temperature-humidity sensor
- HC-SR04 ultrasonic distance sensor
- 16x2 LCD display with I²C backpack (PCF8574)
- LED (built-in GPIO 2 or external)
- Jumper wires and breadboard

## Physical Wiring Photo

![Physical wiring](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/WiringPhoto.png?raw=true)

---

# Software Configuration

### Prerequisites

1. ESP32 with MicroPython firmware installed
2. Wi-Fi network credentials
3. Thonny IDE or similar for file upload

## Setup

1. **Update Wi-Fi Credentials**

Configure your network settings in `boot.py`:

```py
ssid = 'YOUR_WIFI_SSID'        # Line 17
password = 'YOUR_WIFI_PASSWORD' # Line 18
```

2. **Upload Files to ESP32**

- Copy `boot.py` and `main.py` to ESP32 root directory
- Create `lib/` folder on ESP32
- Copy `lib/lcd_api.py` and `lib/machine_i2c_lcd.py` to ESP32 lib folder

3. **Connect Hardware and Run**

- Wire components according to the diagram
- Reset ESP32 to start the web server
- Note the IP address printed in serial console
- Access web interface at that IP address

---

# Features

## Web Interface Controls

- **LED Control**: ON/OFF buttons for remote GPIO control with real-time status
- **Real-time Sensor Display**: Temperature, humidity, and distance with auto-refresh every 3 seconds
- **LCD Display Control**: Show sensor data or custom text on LCD
- **Custom Text Input**: Send messages to LCD with automatic scrolling for long text

## Automatic Behavior

- **Continuous Monitoring**: Real-time sensor data collection and display
- **Auto-refresh**: Web page updates sensor data automatically without page reload
- **Error Handling**: Graceful sensor failure recovery prevents system crashes
- **Text Scrolling**: LCD automatically scrolls messages longer than 16 characters

### Additional Features

- Wi-Fi auto-connection management
- I²C LCD communication with PCF8574 backpack
- JSON API endpoint for sensor data
- URL parameter parsing for multiple web endpoints

---

# Demo

## Task 1: LED Control

![LED Control Web Interface](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task1A.png?raw=true)

![LED on ESP32](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task1B.jpeg?raw=true)

![LED Control Web Interface](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task1C.png?raw=true)

![LED on ESP32](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task1D.jpeg?raw=true)

_Web interface LED control buttons showing GPIO state and real-time status updates_

## Task 2: Sensor Reading

![Real-time Sensor Data Display](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task2.png?raw=true)

_DHT22 temperature/humidity and HC-SR04 distance readings displayed on web page with auto-refresh_

## Task 3: Sensor → LCD

![LCD Display Control Buttons](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task3A.png?raw=true)

![LCD showing temperature data](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task3B.jpeg?raw=true)

![LCD Display Control Buttons](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task3C.png?raw=true)

![LCD showing distance data](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task3D.jpeg?raw=true)

_Buttons to display temperature/humidity or distance data on LCD screen_

## Task 4: Text → LCD

![Custom Text Input Interface](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task4A.png?raw=true)

![LCD displaying custom message](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task4B.jpeg?raw=true)

![Custom Text Input Interface](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task4C.png?raw=true)

![LCD displaying custom message with scrolling](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task4D.jpeg?raw=true)

![LCD displaying custom message with scrolling](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task4E.jpeg?raw=true)

![LCD displaying custom message with scrolling](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%202/assets/Task4F.jpeg?raw=true)

_Custom text input field and LCD displaying user message with scrolling for long text_

## Task 5: Complete System Demo

**Demo Video:**

[![Demo video](https://img.youtube.com/vi/1vdyR_RWGb0/0.jpg)](https://youtu.be/1vdyR_RWGb0)

_The video shows:_

- Complete hardware setup and wiring
- Web interface LED control functionality
- Real-time sensor data monitoring
- LCD display control with sensor data
- Custom text input and scrolling display
- All lab requirements in action

---

# Installation & Usage

1. **Clone the Repository**

```bash
git clone https://github.com/tkimhong/IoT-Group5-Class-Projects
```

2. **Setup Your Hardware:** Follow wiring diagram and reference above
3. **Configure Code:** Update Wi-Fi credentials in `boot.py`
4. **Upload & Run:** Copy all files to ESP32 and execute
5. **Access Web Interface:** Navigate to ESP32's IP address in web browser
