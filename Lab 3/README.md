# IoT Lab 3: ESP32 Environmental Monitoring with BMP280 and Cloud Telemetry

This IoT project demonstrates environmental sensing and cloud-based data visualization using ESP32, BMP280 sensor, and ThingsBoard Cloud platform. The system continuously monitors temperature, atmospheric pressure, and altitude, publishing real-time telemetry data via MQTT for remote monitoring and dashboard visualization.

---

# Hardware Components

- ESP32 Dev Board (flashed with MicroPython firmware)
- BMP280 temperature and barometric pressure sensor
- Jumper wires and breadboard

## Physical Wiring Photo

![Physical wiring](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%203/assets/WiringPhoto.png?raw=true)

### BMP280 Pinout (I²C Mode)

| BMP280 Pin | Description        | ESP32 Pin |
| ---------- | ------------------ | --------- |
| **VCC**    | Power supply       | 3.3V      |
| **GND**    | Ground             | GND       |
| **SCL**    | Serial clock (I²C) | GPIO 22   |
| **SDA**    | Serial data (I²C)  | GPIO 21   |

> **Note:** Some BMP280 modules (e.g., GY-BMP280) include a voltage regulator and can accept 5V. The BMP280 chip itself operates at 3.3V logic.

---

# Software Configuration

### Prerequisites

1. ESP32 with MicroPython firmware installed
2. Wi-Fi network credentials
3. ThingsBoard Cloud account and device access token
4. Thonny IDE or similar for file upload

## Setup Instructions

1. **Create ThingsBoard Device**

   - Sign up/login to [ThingsBoard Cloud](https://thingsboard.cloud/)
   - Navigate to **Devices** → **Add Device**
   - Create a new device (e.g., "ESP32-BMP280")
   - Copy the **Device Access Token** from device credentials

2. **Upload Files to ESP32**

   Upload the following files to your ESP32 using Thonny IDE:
   - `bmp280.py` - BMP280 sensor driver library
   - `main.py` - Main implementation file (auto-runs on boot)

3. **Configure Credentials**

   Update Wi-Fi and ThingsBoard credentials in `main.py`:

   ```python
   WIFI_SSID = "YOUR_WIFI_SSID"        # Your Wi-Fi network name
   WIFI_PASS = "YOUR_WIFI_PASSWORD"    # Your Wi-Fi password
   TB_TOKEN = b"YOUR_DEVICE_TOKEN"     # From ThingsBoard device credentials
   ```

4. **Run the Code**

   - Connect hardware according to wiring diagram
   - Reset ESP32 to auto-run `main.py`
   - Monitor serial output in Thonny REPL
   - Check ThingsBoard dashboard for live telemetry data

---

# Features

## Sensor Monitoring

- **Temperature**: Real-time ambient temperature in degrees Celsius
- **Pressure**: Atmospheric pressure in hPa (hectopascals)
- **Altitude**: Estimated altitude in meters based on barometric formula

## Cloud Integration

- **MQTT Publishing**: Sends sensor data to ThingsBoard Cloud every 5 seconds
- **Real-time Telemetry**: Data visible in ThingsBoard "Latest Telemetry" section
- **Dashboard Visualization**: Create custom widgets and gauges in ThingsBoard

## Automatic Behavior

- **Wi-Fi Auto-connection**: Connects to Wi-Fi on startup with timeout handling
- **Continuous Telemetry**: Publishes sensor readings in JSON format at regular intervals
- **Error Handling**: Graceful recovery from sensor read failures and network issues

---

# Demo

## Task 1: Basic Sensor Testing

Expected output when running `sensor_reading.py` in Thonny REPL:

```
Temp (°C): 25.34
Pressure (hPa): 1013.25
Altitude (m): 123.45
-----------
Temp (°C): 25.36
Pressure (hPa): 1013.26
Altitude (m): 123.42
-----------
```

_BMP280 sensor readings showing temperature, pressure, and altitude every 2 seconds_

## Task 2: MQTT Connection & Publishing

Expected output when running `main.py`:

```
Connecting to Wi-Fi...
Wi-Fi connected: 192.168.1.100
Connecting to ThingsBoard Cloud...
Connected to ThingsBoard: mqtt.thingsboard.cloud
Published to ThingsBoard: Temp=25.34°C, Pressure=1013.25hPa, Alt=123.45m
Published to ThingsBoard: Temp=25.36°C, Pressure=1013.26hPa, Alt=123.42m
Published to ThingsBoard: Temp=25.35°C, Pressure=1013.24hPa, Alt=123.44m
```

_Successful Wi-Fi connection and MQTT publishing to ThingsBoard Cloud every 5 seconds_

## Task 3: ThingsBoard Telemetry

In ThingsBoard Cloud, navigate to your device and check the "Latest Telemetry" tab. You should see:

- `temperature`: Real-time values updating every 5 seconds
- `pressure`: Real-time values updating every 5 seconds
- `altitude`: Real-time values updating every 5 seconds

_All three metrics should show recent timestamps and reasonable values_

## Task 4: ThingsBoard Dashboard

![ThingsBoard dashboard with visualization widgets](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%203/assets/Dashboard.png?raw=true)

_Custom dashboard with temperature gauge, pressure chart, and altitude display_

## Complete System Demo

**Demo Video:**

[![Demo video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

_The video demonstrates:_
- Hardware setup and BMP280 wiring
- Sensor reading verification
- MQTT connection and data publishing
- ThingsBoard dashboard with live updates

---

# Technical Details

## BMP280 Sensor

The BMP280 is a digital barometric pressure and temperature sensor by Bosch Sensortec.

| Feature               | Specification              |
| --------------------- | -------------------------- |
| **Pressure Range**    | 300 - 1100 hPa             |
| **Temperature Range** | -40°C to +85°C             |
| **Accuracy**          | ±1 hPa (≈ ±8m altitude)    |
| **Operating Voltage** | 1.8V - 3.6V (3.3V typical) |
| **Communication**     | I²C (address 0x76 or 0x77) |
| **Power Consumption** | Ultra-low, ideal for IoT   |

**How it Works:**
- Measures absolute atmospheric pressure using piezo-resistive sensor
- Calculates altitude from pressure using barometric formula:
  ```
  altitude = 44330 × (1 - (p/101325)^(1/5.255))
  ```
- Temperature compensation applied to pressure readings for accuracy

## MQTT Protocol Overview

**MQTT (Message Queuing Telemetry Transport)** is a lightweight publish-subscribe messaging protocol for IoT.

### Key Concepts

| Term          | Description                                                            |
| ------------- | ---------------------------------------------------------------------- |
| **Broker**    | MQTT server that routes messages (e.g., ThingsBoard Cloud)             |
| **Topic**     | Hierarchical string identifying data (e.g., `v1/devices/me/telemetry`) |
| **Publish**   | Sending a message to a topic                                           |
| **QoS**       | Quality of Service level (0, 1, or 2)                                  |
| **Client ID** | Unique identifier for MQTT client                                      |

### ThingsBoard MQTT Authentication

- **Username**: Device access token (from ThingsBoard)
- **Password**: Empty string (`b""`)
- **Topic**: `v1/devices/me/telemetry` (for device telemetry)
- **Payload**: JSON-encoded sensor data

---

# Installation & Usage

1. **Clone the Repository**

```bash
git clone https://github.com/tkimhong/IoT-Group5-Class-Projects
```

2. **Setup Your Hardware:** Follow wiring diagram and reference above
3. **Configure Code:** Update Wi-Fi and ThingsBoard credentials in `main.py`
4. **Upload & Run:** Copy `bmp280.py` and `main.py` to ESP32 and reset the board
5. **Create Dashboard:** Login to ThingsBoard Cloud and visualize your device telemetry
