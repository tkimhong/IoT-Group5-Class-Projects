import network, time
from umqtt.simple import MQTTClient
from machine import Pin, I2C
from bmp280 import BMP280
import time
import json

i2c = I2C(0, scl=Pin(21), sda=Pin(22))
bmp = BMP280(i2c, addr=0x76)

# TODO: Configure these before uploading to ESP32
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"

BROKER = "test.mosquitto.org"
PORT = 1883
CLIENT_ID = b"esp32_YOUR_GROUP_ID"
TOPIC = b"/YOUR_TOPIC_PATH/esp32/sensor"
KEEPALIVE = 30


def wifi_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        t0 = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t0) > 20000:
                raise RuntimeError("Wi-Fi connect timeout")
            time.sleep(0.3)
    print("WiFi OK:", wlan.ifconfig())
    return wlan


def make_client():
    return MQTTClient(
        client_id=CLIENT_ID, server=BROKER, port=PORT, keepalive=KEEPALIVE
    )


def connect_mqtt(c):
    time.sleep(0.5)
    c.connect()
    print("MQTT connected")


def main():
    wifi_connect()
    client = make_client()
    while True:
        try:
            connect_mqtt(client)
            while True:
                value = bmp.temperature
                value2 = bmp.pressure / 100
                value3 = bmp.altitude
                msg1 = {
                    "temperature": round(value, 2),
                    "pressure": value2,
                    "altitude": value3,
                }
                msg = json.dumps(msg1)
                client.publish(TOPIC, msg)
                print("Sent:", msg)
                time.sleep(5)
        except OSError as e:
            print("MQTT error:", e)
            try:
                client.close()
            except:
                pass
            print("Retrying MQTT in 3s...")
            time.sleep(3)


main()
