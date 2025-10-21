# bmp280_thingsboard.py - Publish BMP280 sensor data to ThingsBoard Cloud
import network
import time
import json
from machine import Pin, I2C
from bmp280 import BMP280
from umqtt.simple import MQTTClient

# ===== Wi-Fi credentials =====
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASS = "YOUR_WIFI_PASSWORD"

# ===== ThingsBoard Cloud setup =====
TB_HOST = "mqtt.thingsboard.cloud"
TB_PORT = 1883
TB_TOKEN = b"YOUR_DEVICE_ACCESS_TOKEN"  # Get this from ThingsBoard device credentials
TOPIC = b"v1/devices/me/telemetry"

# ===== I2C and BMP280 setup =====
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bmp = BMP280(i2c, addr=0x76)

# ===== Connect Wi-Fi =====
def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > 15000:
                raise RuntimeError("Wi-Fi connection timeout")
            time.sleep(0.2)
    print("Wi-Fi connected:", wlan.ifconfig()[0])

# ===== Main =====
def main():
    wifi_connect()

    # Connect to ThingsBoard (username = token, password empty)
    print("Connecting to ThingsBoard Cloud...")
    client = MQTTClient(
        b"esp32-bmp280-tb",
        TB_HOST,
        port=TB_PORT,
        user=TB_TOKEN,
        password=b"",
        keepalive=30,
        ssl=False
    )
    client.connect()
    print("Connected to ThingsBoard:", TB_HOST)

    # Publish sensor data every 5 seconds
    while True:
        try:
            # Read sensor values
            temperature = round(bmp.temperature, 2)
            pressure = round(bmp.pressure / 100, 2)  # Convert Pa to hPa
            altitude = round(bmp.altitude, 2)

            # Create JSON payload (ThingsBoard expects key-value pairs)
            payload = json.dumps({
                "temperature": temperature,
                "pressure": pressure,
                "altitude": altitude
            }).encode("utf-8")

            # Publish to ThingsBoard
            client.publish(TOPIC, payload)
            print(f"Published to ThingsBoard: Temp={temperature}°C, Pressure={pressure}hPa, Alt={altitude}m")

            time.sleep(5)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
