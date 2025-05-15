import network
import time
import machine
import uasyncio as asyncio
from machine import Pin, PWM, I2C
from umqtt.simple import MQTTClient

# ===== Configuration =====
WIFI_SSID = 'WIFI_ID'
WIFI_PASSWORD = 'WIFI_Password'

# ===== Adafruit IO MQTT Configuration =====
ADAFRUIT_USERNAME = 'Adafruit_Username'
ADAFRUIT_AIO_KEY = 'Adafruit_Key'
MQTT_BROKER = 'io.adafruit.com'
CLIENT_ID = 'picoW-client'
TEMP_FEED = f'{ADAFRUIT_USERNAME}/feeds/temperature'
FAN_FEED = f'{ADAFRUIT_USERNAME}/feeds/fan'

# ===== Hardware Setup =====
fan_pwm = PWM(Pin(16))
fan_pwm.freq(1000)

led_red = PWM(Pin(17))
led_green = PWM(Pin(18))
led_blue = PWM(Pin(19))
for led in [led_red, led_green, led_blue]:
    led.freq(1000)

# ===== Display Setup =====
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
oled = None

def init_display():
    global oled
    try:
        from ssd1306 import SSD1306_I2C
        oled = SSD1306_I2C(128, 64, i2c)
        oled.fill(0)
        oled.text("Display Init OK", 0, 0)
        oled.show()
        return oled
    except Exception as e:
        print("Display init failed:", e)
        return None

def display(text, line=0, clear_line=True):
    global oled
    if oled is None:
        oled = init_display()
        if oled is None:
            return
    if clear_line:
        oled.fill_rect(0, line * 10, 128, 10, 0)
    oled.text(text, 0, line * 10)
    oled.show()

# ===== WiFi Connection =====
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    time.sleep(1)

    if not wlan.isconnected():
        display("Connecting WiFi", 0)
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        for _ in range(15):
            if wlan.isconnected():
                break
            time.sleep(1)
    
    if wlan.isconnected():
        ip = wlan.ifconfig()[0]
        display(f"IP: {ip}", 1)
        return True
    else:
        display("WiFi Failed", 1)
        return False

# ===== MQTT Setup =====
fan_on = False
client = None

def mqtt_callback(topic, msg):
    global fan_on
    topic = topic.decode()
    msg = msg.decode().upper()
    if topic == FAN_FEED:
        fan_on = (msg == "ON")
        print(f"Fan toggle received: {msg}")

def connect_mqtt():
    global client
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, user=ADAFRUIT_USERNAME, password=ADAFRUIT_AIO_KEY)
    client.set_callback(mqtt_callback)
    client.connect()
    client.subscribe(FAN_FEED)
    display("MQTT OK", 2)

# ===== Main Control Logic =====
async def main_loop():
    while True:
        try:
            client.check_msg()  # Handle MQTT messages

            # Simulated temperature
            temp = 24.5 + (time.ticks_ms() % 1000) / 100.0
            
            # Control fan strictly by toggle
            if fan_on:
                fan_pwm.duty_u16(65535)
                led_red.duty_u16(65535)
                led_green.duty_u16(0)
            else:
                fan_pwm.duty_u16(0)
                led_red.duty_u16(0)
                led_green.duty_u16(65535)

            led_blue.duty_u16(65535)  # Always off

            # Update display
            display(f"Temp: {temp:.1f}C", 0)
            display(f"Fan: {'ON ' if fan_on else 'OFF'}", 1)
            display("Status:", 2)
            display("Manual Mode", 3)

            # Only publish temperature
            client.publish(TEMP_FEED, str(temp))

            await asyncio.sleep(2)

        except Exception as e:
            print("Loop error:", e)
            display("Error", 0)
            await asyncio.sleep(5)

# ===== Main Entry Point =====
async def main():
    for led in [led_red, led_green, led_blue]:
        led.duty_u16(65535)

    init_display()
    await asyncio.sleep(1)

    if not connect_wifi():
        display("WiFi Fail", 0)
        await asyncio.sleep(5)
        machine.reset()

    try:
        connect_mqtt()
    except Exception as e:
        display("MQTT Fail", 2)
        await asyncio.sleep(5)
        machine.reset()

    await main_loop()

# Run the program
try:
    asyncio.run(main())
except Exception as e:
    display("Crash", 0)
    time.sleep(5)
    machine.reset()

