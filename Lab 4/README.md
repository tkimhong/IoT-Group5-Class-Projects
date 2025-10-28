# IoT Group 5 Lab 4: ESP32 Environmental Monitoring with Local Data Pipeline

This IoT project demonstrates a complete local data pipeline using ESP32 with BMP280 sensor, publishing environmental telemetry via MQTT to Node-RED, storing time-series data in InfluxDB, and visualizing real-time metrics in Grafana dashboards.

---

## Architecture Overview

```
ESP32 (MicroPython + BMP280)
    ↓ MQTT Publish (JSON payload)
MQTT Broker (test.mosquitto.org:1883)
    ↓ Subscribe to topic
Node-RED (Flow-based automation)
    ↓ Transform & store
InfluxDB 1.x (Time-series database)
    ↓ Query with InfluxQL
Grafana (Visualization dashboard)
```

---

## Hardware Components

- **ESP32 Dev Board** (flashed with MicroPython firmware)
- **BMP280** temperature and barometric pressure sensor
- **Jumper wires** and breadboard

### BMP280 Wiring (I2C Mode)

| BMP280 Pin | Description        | ESP32 Pin |
| ---------- | ------------------ | --------- |
| **VCC**    | Power supply       | 3.3V      |
| **GND**    | Ground             | GND       |
| **SCL**    | Serial clock (I2C) | GPIO 21   |
| **SDA**    | Serial data (I2C)  | GPIO 22   |

> The BMP280 communicates via I2C at address `0x76` (default) or `0x77`

### Physical Wiring Photo

![Physical wiring](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%204/assets/WiringPhoto.png?raw=true)

---

## Software Stack

### Prerequisites

- **ESP32** with MicroPython firmware installed
- **Node.js >= 14** and **npm** for Node-RED installation
- **InfluxDB 1.x** (v1.12.2 recommended)
- **Grafana v10+** for dashboard visualization
- **Thonny IDE** (or mpremote/ampy) for uploading MicroPython scripts

### Optional Tools

- **MQTT Explorer** - Debug and monitor MQTT topics in real-time

---

## Installation Guide

### 1. Install Node-RED

Node-RED is a flow-based automation server for wiring together IoT devices and APIs.

```bash
# Install Node-RED globally via npm
npm install -g --unsafe-perm node-red

# Start Node-RED server
node-red
```

Access Node-RED at: [http://localhost:1880](http://localhost:1880)

**Required Palette:**
- Install `node-red-contrib-influxdb` via **Menu → Manage palette → Install**

---

### 2. Install InfluxDB 1.x (Windows)

InfluxDB is a time-series database optimized for IoT sensor data.

> Tested with **InfluxDB v1.12.2** using InfluxQL syntax

**Download & Install:**

```powershell
# Download InfluxDB 1.12.2 for Windows
wget https://download.influxdata.com/influxdb/releases/v1.12.2/influxdb-1.12.2-windows.zip -UseBasicParsing -OutFile influxdb-1.12.2-windows.zip

# Extract to Program Files
Expand-Archive .\influxdb-1.12.2-windows.zip -DestinationPath 'C:\Program Files\InfluxData\influxdb\'
```

**Start InfluxDB Server:**

```powershell
cd "C:\Program Files\InfluxData\influxdb"
.\influxd.exe
```

**Open InfluxDB Shell (new PowerShell window):**

```powershell
cd "C:\Program Files\InfluxData\influxdb"
.\influx.exe -host 127.0.0.1
```

**Create Database:**

```sql
CREATE DATABASE aupp_lab;
SHOW DATABASES;
USE aupp_lab;
```

---

### 3. Install Grafana (Windows)

Grafana provides powerful visualization dashboards for time-series data.

> Tested with **Grafana v10+** using InfluxQL queries

**Download & Install:**

1. Download Windows installer: [Grafana Download](https://grafana.com/grafana/download?platform=windows)
2. Run `grafana-enterprise-<version>.windows-amd64.msi` and accept defaults
3. Grafana installs as a Windows Service and starts automatically

**Verify Service:**

```powershell
# Check if Grafana service is running
net start grafana
```

**Access Grafana:**

Open [http://localhost:3000](http://localhost:3000)

- **Default Username:** `admin`
- **Default Password:** `admin` (you'll be prompted to change it)

---

## Project Setup

### Step 1: Configure ESP32 Code

**Files Required:**
- [main.py](main.py) - Main application with WiFi, MQTT, and sensor logic
- [bmp280.py](bmp280.py) - BMP280 sensor driver library

**Update Credentials in main.py:**

```python
# TODO: Configure these before uploading to ESP32
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"

BROKER = "test.mosquitto.org"
PORT = 1883
CLIENT_ID = b"esp32_YOUR_GROUP_ID"      # Make this unique!
TOPIC = b"/YOUR_TOPIC_PATH/esp32/sensor"  # Make this unique!
KEEPALIVE = 30
```

**Upload to ESP32:**

1. Open **Thonny IDE**
2. Connect ESP32 via USB
3. Upload both `bmp280.py` and `main.py` to ESP32 filesystem
4. Reset ESP32 - code runs automatically on boot

**Expected Serial Output:**

```
Connecting to WiFi...
WiFi OK: ('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8')
MQTT connected
Sent: {"temperature": 25.43, "pressure": 1013.25, "altitude": 123.45}
Sent: {"temperature": 25.44, "pressure": 1013.26, "altitude": 123.42}
```

---

### Step 2: Node-RED Flow Configuration

**Start Node-RED:**

```bash
node-red
```

Access at [http://localhost:1880](http://localhost:1880)

**Create Flow:**

1. **MQTT In Node**
   - Drag `mqtt in` node to canvas
   - **Server:** `test.mosquitto.org:1883`
   - **Topic:** Match your ESP32 topic (e.g., `/YOUR_TOPIC_PATH/esp32/sensor`)
   - **QoS:** 0

2. **Function Node** (Transform payload)
   - Drag `function` node to canvas
   - Add transformation code:

   ```javascript
   msg.measurement = "random";
   msg.payload = { value: Number(msg.payload) };
   return msg;
   ```

3. **InfluxDB Out Node**
   - Drag `influxdb out` node to canvas
   - **Database:** `aupp_lab`
   - **Measurement:** `random`
   - **URL:** `http://127.0.0.1:8086`
   - **Version:** 1.x

4. **Debug Node** (Optional)
   - Connect to MQTT output to verify incoming data

**Deploy Flow:**

Click **Deploy** button in top-right corner

---

### Step 3: Verify Data in InfluxDB

**Query Recent Data:**

```sql
USE aupp_lab;
SELECT * FROM random ORDER BY time DESC LIMIT 5;
```

**Expected Output:**

```
time                  value
----                  -----
2025-10-28T10:30:45Z  25.43
2025-10-28T10:30:40Z  25.44
2025-10-28T10:30:35Z  25.42
```

---

### Step 4: Grafana Dashboard Setup

**Add InfluxDB Data Source:**

1. Navigate to **Settings (⚙️) → Data Sources**
2. Click **Add data source**
3. Select **InfluxDB**
4. Configure connection:

   | Setting            | Value                   |
   | ------------------ | ----------------------- |
   | **Query Language** | InfluxQL                |
   | **URL**            | `http://127.0.0.1:8086` |
   | **Database**       | `aupp_lab`              |
   | **HTTP Method**    | GET                     |
   | **Version**        | 1.8+                    |

5. Click **Save & Test**

**Create Dashboard:**

1. Click **+ (Create) → Dashboard → Add new panel**
2. Select **InfluxDB - aupp_lab** as data source
3. In query editor:
   - **FROM:** `random`
   - **SELECT:** `field(value)` with `mean()` aggregation
   - **GROUP BY:** `time($__interval)` and `fill(null)`
4. Set panel title (e.g., "ESP32 Sensor Data")
5. Configure refresh interval (e.g., 5s auto-refresh)
6. Click **Apply** and **Save dashboard**

![Grafana Dashboard Example](https://github.com/tkimhong/IoT-Group5-Class-Projects/blob/main/Lab%204/assets/GrafanaDashboard.png?raw=true)

---

## Demo

### Video Demonstration

**Full System Demo:**

[![Lab 4 Demo Video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

> TODO Replace `VIDEO_ID` with YouTube video ID

**Demo Contents:**
- ESP32 hardware setup and BMP280 wiring
- WiFi connection and MQTT publishing verification
- Node-RED flow configuration and deployment
- InfluxDB data verification
- Grafana dashboard creation and real-time visualization

---

## Features

### Real-time Environmental Monitoring

- **Temperature:** Ambient temperature in degrees Celsius
- **Pressure:** Atmospheric pressure in hPa (hectopascals)
- **Altitude:** Estimated altitude in meters (barometric formula)

### Data Pipeline

- **MQTT Publishing:** ESP32 publishes JSON payloads every 5 seconds
- **Node-RED Processing:** Subscribes to MQTT topic and transforms data
- **InfluxDB Storage:** Time-series data with millisecond precision
- **Grafana Visualization:** Real-time dashboards with auto-refresh

### Automatic Recovery

- **WiFi Auto-reconnect:** 20-second timeout with retry logic
- **MQTT Auto-reconnect:** Handles OSError with 3-second retry delay
- **Continuous Operation:** Publishes data indefinitely with error handling

---

## Troubleshooting

### ESP32 Issues

**WiFi connection timeout:**
- Verify SSID and password in [main.py:12-13](main.py#L12-L13)
- Check router is powered on and within range
- WiFi timeout is 20 seconds

**MQTT connection fails:**
- ESP32 auto-retries every 3 seconds
- Verify `test.mosquitto.org` is accessible
- Check topic name matches Node-RED subscription

**BMP280 sensor errors:**
- Verify wiring: SCL→GPIO21, SDA→GPIO22, VCC→3.3V, GND→GND
- Check I2C address (default 0x76, some modules use 0x77)
- Run basic sensor test in Thonny REPL

### Node-RED Issues

**MQTT In node not receiving data:**
- Check MQTT broker address and port
- Verify topic matches ESP32 publish topic
- Use MQTT Explorer to debug topic

**InfluxDB Out node errors:**
- Verify InfluxDB server is running on port 8086
- Check database `aupp_lab` exists
- Ensure function node transforms payload correctly

### InfluxDB Issues

**Connection refused:**
- Ensure `influxd.exe` is running
- Check port 8086 is not blocked by firewall
- Verify database was created with `CREATE DATABASE aupp_lab;`

**No data showing in queries:**
- Check Node-RED debug panel for errors
- Verify measurement name is `random`
- Ensure Node-RED flow is deployed

### Grafana Issues

**Data source connection fails:**
- Verify InfluxDB URL: `http://127.0.0.1:8086`
- Check database name matches: `aupp_lab`
- Use InfluxQL (not Flux) for InfluxDB 1.x

**Dashboard shows no data:**
- Verify data exists in InfluxDB with `SELECT * FROM random;`
- Check query syntax in Grafana panel
- Ensure time range includes recent data

---

## Technical Details

### BMP280 Sensor Specifications

| Feature               | Specification              |
| --------------------- | -------------------------- |
| **Pressure Range**    | 300 - 1100 hPa             |
| **Temperature Range** | -40°C to +85°C             |
| **Accuracy**          | ±1 hPa (≈ ±8m altitude)    |
| **Operating Voltage** | 1.8V - 3.6V (3.3V typical) |
| **Communication**     | I2C (address 0x76 or 0x77) |
| **Power Consumption** | Ultra-low, ideal for IoT   |

**Altitude Calculation:**
```
altitude = 44330 × (1 - (pressure/101325)^(1/5.255))
```

### MQTT Protocol

**Configuration:**
- **Broker:** `test.mosquitto.org` (public, no authentication)
- **Port:** 1883 (non-TLS)
- **QoS:** 0 (at most once delivery)
- **Payload Format:** JSON with temperature, pressure, altitude

**Example Payload:**
```json
{
  "temperature": 25.43,
  "pressure": 1013.25,
  "altitude": 123.45
}
```

### InfluxDB Schema

- **Database:** `aupp_lab`
- **Measurement:** `random`
- **Field:** `value` (numeric sensor reading)
- **Time Precision:** Nanoseconds (default)