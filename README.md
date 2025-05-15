# IoT Home Controller with Raspberry Pi Pico W

### Embedded IoT Control System Architecture and Real-Time Data Integration using MQTT and Adafruit IO

**Author:** Sangwon LEE

---

## 📦 Project Overview

This project implements a Wi-Fi-enabled IoT home controller using a Raspberry Pi Pico W. The system monitors temperature, controls a fan motor and RGB LED, and provides a dashboard interface via Adafruit IO. The Pico W interacts with the cloud using MQTT for remote control and displays live data on an OLED screen.

---

## 📋 Detailed Objectives

* Establish a reliable Wi-Fi connection using SSID and password.
* Implement secure MQTT communication using Adafruit IO credentials.
* Simulate temperature readings using a custom algorithm ranging from 24.5°C to 34.5°C.
* Display real-time system status on a 0.96-inch OLED display using the SSD1306 driver.
* Provide fan control via Adafruit IO dashboard toggle switches.
* Enable RGB LED brightness adjustment via PWM, linked to Adafruit IO slider inputs.
* Implement error handling, data synchronization, and system recovery using `uasyncio`.

---

## 🛠️ Hardware Setup & Wiring

### Components and Pin Assignments:

| Component         | Function   | Pico Pin | Notes              |
| ----------------- | ---------- | -------- | ------------------ |
| OLED Display      | I2C SDA    | GP4      | Shared with LM75B  |
| OLED Display      | I2C SCL    | GP5      | Shared with LM75B  |
| Fan Motor         | PWM Output | GP16     | Controlled via PWM |
| RGB LED Red       | PWM Output | GP17     | 220Ω resistor      |
| RGB LED Green     | PWM Output | GP18     | 220Ω resistor      |
| RGB LED Blue      | PWM Output | GP19     | 220Ω resistor      |
| LM75B Temp Sensor | I2C SDA    | GP4      | Shared with OLED   |
| LM75B Temp Sensor | I2C SCL    | GP5      | Shared with OLED   |

### Power Connections:

* Power Source: USB 5V (for Pico W and peripherals)
* Shared Ground for all components
* 3.3V power rail for LM75B and OLED display

---

## 🌐 Adafruit IO Setup

### 1. Create an Adafruit IO Account

* Go to [Adafruit IO](https://io.adafruit.com/) and sign up for a free account.
* Once logged in, navigate to **My Key** in the profile menu to find your **Adafruit IO Key**. Keep this key secure, as it is used to authenticate your device.

### 2. Create Feeds

* Go to **Feeds > New Feed** and create the following feeds:

  * `temperature` – For temperature data publishing.
  * `fan` – For fan control (ON/OFF commands).
  * `led-red` – For controlling the Red LED channel (0-255).
  * `led-green` – For controlling the Green LED channel (0-255).
  * `led-blue` – For controlling the Blue LED channel (0-255).

### 3. Create a Dashboard

* Navigate to **Dashboards > New Dashboard** and name it `IoT Home Controller`.
* Add the following widgets to the dashboard:

  * **Gauge Widget** for `temperature` feed to display real-time temperature.
  * **Toggle Switch** for `fan` feed to control the fan ON/OFF.
  * **Slider Widgets** for `led-red`, `led-green`, `led-blue` feeds to adjust LED brightness.

### 4. Link Widgets to Feeds

* While setting up each widget, select the corresponding feed from the list.
* Configure the slider widgets to range from `0` to `255` for LED brightness control.
* Ensure that the `temperature` gauge displays values from `24` to `35` to match the simulated temperature range.

### 5. MQTT Integration

* Go to **My Key** and copy the following details:

  * **Adafruit IO Username** 
  * **Adafruit IO Key:** The private key generated during setup.
  * **MQTT Broker URL:** `io.adafruit.com`
  * **Ports** 

---

## 🧑‍💻 Embedded Software Implementation

**Language:** MicroPython
**IDE:** Thonny IDE

### Libraries Used:

* `network` – Wi-Fi management
* `time` – Timing and delays
* `machine` – GPIO and PWM control
* `uasyncio` – Non-blocking, cooperative multitasking
* `umqtt.simple` – MQTT communication
* `ssd1306` – OLED display driver

### Key Functions:

1. **Wi-Fi Connection:** Establishes connection using SSID and password.
2. **MQTT Client:** Connects to Adafruit IO, subscribes to `fan`, `led-red`, `led-green`, `led-blue` feeds.
3. **Temperature Simulation:** Generates temperature data between 24.5°C and 34.5°C every 5 seconds.
4. **Fan Control:** Toggles fan ON/OFF based on MQTT messages.
5. **RGB LED Control:** Adjusts PWM duty cycle of RGB LEDs based on MQTT slider values.
6. **OLED Display Update:** Displays temperature, fan state, and RGB values.

---

## 🖥️ Code Structure & Implementation Details

* `main.py`: Core logic, Wi-Fi connection, and MQTT subscription.
* `ssd1306.py`: SSD1306 OLED driver implementation for I2C and SPI communication.
* `config.py`: Stores Wi-Fi and Adafruit IO credentials.

### Example: Wi-Fi Configuration in `config.py`

```python
WIFI_SSID = 'WIFI_ID'
WIFI_PASSWORD = 'WIFI_Password'
ADAFRUIT_USERNAME = 'Adafruit_Username'
ADAFRUIT_AIO_KEY = 'Adafruit_key'
```

### Example: Main Control Loop in `main.py`

```python
async def main_loop():
    while True:
        client.check_msg()
        temp = read_temp()
        fan_pwm.duty_u16(65535 if fan_on else 0)
        display([
            f"Temp: {temp:.1f}C",
            f"Fan: {'ON' if fan_on else 'OFF'}",
            f"LED: R{red_val} G{green_val} B{blue_val}"
        ])
        client.publish(TEMP_FEED, str(temp))
        await asyncio.sleep(5)
```

---

## 🧪 Testing & Results

* Wi-Fi connection time: 10 seconds
* MQTT communication latency: <200ms
* Temperature accuracy: ±0.5°C
* OLED refresh rate: 5 seconds
* PWM response: Real-time adjustment based on Adafruit IO inputs

---

## 🚀 Future Work

* Integrate additional sensors: Humidity, motion, and ambient light sensors.
* Implement TLS encryption for MQTT to secure communication.
* Add a data logging feature for long-term monitoring.
* Expand control logic to automate fan based on temperature thresholds.

---

## 📚 References

* [MicroPython Documentation](https://docs.micropython.org/)
* [Adafruit IO MQTT API](https://io.adafruit.com/api/docs/mqtt.html)

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.






















