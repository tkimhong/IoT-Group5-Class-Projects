# Complete project details at https://RandomNerdTutorials.com

import machine
import dht
import time
import socket
from machine import Pin, SoftI2C, time_pulse_us
from machine_i2c_lcd import I2cLcd
from time import sleep_us

# LED setup
led = Pin(2, Pin.OUT)

# Global sensor variables
current_temp = 0
current_humidity = 0
current_distance = 0

# LCD display mode tracking
lcd_mode = "off"  # "temp", "distance", "custom", "off"
lcd_text = ""
scroll_position = 0
scroll_counter = 0

# Sensor setup
dht_sensor = dht.DHT22(Pin(4))
TRIG = Pin(27, Pin.OUT)
ECHO = Pin(26, Pin.IN)

# LCD setup
I2C_ADDR = 0x27
i2c = SoftI2C(sda=Pin(21), scl=Pin(22), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

def read_sensors():
    global current_temp, current_humidity, current_distance
    
    # Read DHT22
    try:
        dht_sensor.measure()
        current_temp = dht_sensor.temperature()
        current_humidity = dht_sensor.humidity()
    except OSError:
        current_temp = 0
        current_humidity = 0
    
    # Read ultrasonic
    TRIG.off(); sleep_us(2)
    TRIG.on(); sleep_us(10)
    TRIG.off()
    t = time_pulse_us(ECHO, 1, 30000)
    current_distance = (t * 0.0343) / 2.0 if t > 0 else 0

def update_lcd():
    global lcd_mode, lcd_text, scroll_position, scroll_counter
    if lcd_mode == "temp":
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr('Temp: {:.1f}C'.format(current_temp))
        lcd.move_to(0, 1)
        lcd.putstr('Humidity: {:.1f}%'.format(current_humidity))
    elif lcd_mode == "distance":
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr('Distance:')
        lcd.move_to(0, 1)
        lcd.putstr('{:.1f} cm'.format(current_distance))
    elif lcd_mode == "custom" and lcd_text:
        if len(lcd_text) <= 16:
            # Short text, no scrolling needed
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(lcd_text)
        else:
            # Long text, implement scrolling
            scroll_counter += 1
            if scroll_counter >= 3:  # Scroll every 3 web requests (roughly 9 seconds)
                scroll_counter = 0
                scroll_position += 1
                if scroll_position > len(lcd_text) - 16:
                    scroll_position = 0
            
            display_text = lcd_text[scroll_position:scroll_position + 16]
            if len(display_text) < 16:
                display_text += lcd_text[:16 - len(display_text)]
            
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr(display_text)

def web_page():
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html = """<html><head> <title>ESP IoT Lab Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.2rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 12px 30px; text-decoration: none; font-size: 18px; margin: 5px; cursor: pointer;}
  .button2{background-color: #4286f4;}.button3{background-color: #28a745;}.sensor{background-color: #f8f9fa; padding: 10px; margin: 10px; border-radius: 5px;}
  input[type=text]{padding: 8px; margin: 5px; font-size: 16px; width: 200px;}</style></head><body> 
  <h1>ESP32 IoT Lab Control</h1> 
  
  <div class="sensor"><h3>LED Control</h3>
  <p>GPIO state: <strong>""" + gpio_state + """</strong></p>
  <p><a href="/?led=on"><button class="button">LED ON</button></a>
  <a href="/?led=off"><button class="button button2">LED OFF</button></a></p></div>
  
  <div class="sensor"><h3>Sensor Readings</h3>
  <p>Temperature: <strong><span id="temp">""" + "{:.2f}".format(current_temp) + """</span> deg C</strong></p>
  <p>Humidity: <strong><span id="humidity">""" + "{:.2f}".format(current_humidity) + """</span>%</strong></p>
  <p>Distance: <strong><span id="distance">""" + "{:.2f}".format(current_distance) + """</span> cm</strong></p></div>
  
  <div class="sensor"><h3>LCD Display Control</h3>
  <p><a href="/?show=temp"><button class="button button3">Show Temp on LCD</button></a>
  <a href="/?show=distance"><button class="button button3">Show Distance on LCD</button></a></p>
  <form action="/" method="get">
  <input type="text" name="lcd_text" placeholder="Enter custom message" maxlength="32">
  <button type="submit" class="button">Send to LCD</button></form></div>
  
  <script>
  function updateSensors() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/?data=sensors', true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var data = JSON.parse(xhr.responseText);
        document.getElementById('temp').textContent = data.temp;
        document.getElementById('humidity').textContent = data.humidity;
        document.getElementById('distance').textContent = data.distance;
      }
    };
    xhr.send();
  }
  setInterval(updateSensors, 3000);
  </script>
  </body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  # Read sensors before processing request
  read_sensors()
  # Update LCD if in auto-update mode
  update_lcd()
  
  # Parse URL parameters
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  show_temp = request.find('/?show=temp')
  show_distance = request.find('/?show=distance')
  lcd_text_start = request.find('/?lcd_text=')
  sensor_data = request.find('/?data=sensors')
  
  # LED control
  if led_on == 6:
    print('LED ON')
    led.value(1)
  if led_off == 6:
    print('LED OFF')
    led.value(0)
  
  # LCD control
  if show_temp == 6:
    print('Showing temperature on LCD')
    lcd_mode = "temp"
    update_lcd()
  elif show_distance == 6:
    print('Showing distance on LCD')
    lcd_mode = "distance"
    update_lcd()
  elif lcd_text_start == 6:
    # Extract text from URL after the = sign
    equals_pos = request.find('=', lcd_text_start)
    text_end = request.find(' HTTP')
    if equals_pos > 0 and text_end > equals_pos + 1:
      text = request[equals_pos + 1:text_end].replace('%20', ' ').replace('+', ' ')
      print('Displaying custom text:', text)
      lcd_mode = "custom"
      lcd_text = text
      scroll_position = 0
      scroll_counter = 0
      update_lcd()
  
  # Handle sensor data request
  if sensor_data == 6:
    response = '{"temp":"' + "{:.2f}".format(current_temp) + '","humidity":"' + "{:.2f}".format(current_humidity) + '","distance":"' + "{:.2f}".format(current_distance) + '"}'
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: application/json\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
  else:
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
  conn.close()
