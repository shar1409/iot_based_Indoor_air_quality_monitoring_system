# 🌫️ IoT-Based Indoor Air Quality Monitoring System

A low-cost, portable IoT system for monitoring indoor air quality, built with **Raspberry Pi Pico W**, **MQ7 (CO)**, and **MQ135 (CO₂/VOCs)** sensors.  
It calculates an **Indoor Air Quality Index (IAQI)**, logs data to **ThingSpeak**, sends **Telegram alerts**, and uses **LEDs and a buzzer** for local notifications.

---

## 🌟 Features

- **Sensors**  
  - **MQ7**: Detects carbon monoxide (CO) in ppm  
  - **MQ135**: Measures CO₂ and VOCs (approximated as CO₂ in ppm)

- **IAQI Calculation**: Uses EPA breakpoints for CO and custom indoor breakpoints for CO₂  
- **Alerts**: Sends Telegram notifications when CO > 50 ppm or CO₂ > 1000 ppm  
- **Data Logging**: Uploads CO and CO₂ data to **ThingSpeak** for visualization  
- **Indicators**:  
  - Green LED: Safe air  
  - Red LED + Buzzer: Poor air quality  

---

## 🛠️ Hardware Requirements

- Raspberry Pi Pico W  
- MQ7 CO sensor module  
- MQ135 CO₂/multi-gas sensor module  
- Active buzzer  
- Green and Red LEDs (with ~220Ω resistors)  
- Voltage divider resistors (2.2kΩ and 3.3kΩ)  
- Breadboard and jumper wires  

---

## 🔌 Connections

| Component         | Pin Type     | GPIO       | Pico W Pin |
|------------------|--------------|------------|------------|
| MQ7 AO           | Analog Out   | GPIO26     | Pin 31     |
| MQ7 DO           | Digital Out  | GPIO15     | Pin 20     |
| MQ7 VCC          | Power (5V)   | VBUS       | Pin 40     |
| MQ7 GND          | Ground       | GND        | Pin 38     |
| MQ135 AO         | Analog Out   | GPIO27     | Pin 32     |
| MQ135 DO         | Digital Out  | GPIO16     | Pin 21     |
| MQ135 VCC        | Power (5V)   | VBUS       | Pin 40     |
| MQ135 GND        | Ground       | GND        | Pin 38     |
| Buzzer +         | Signal       | GPIO18     | Pin 24     |
| Buzzer -         | Ground       | GND        | Pin 38     |
| Green LED Anode  | Signal       | GPIO19     | Pin 25     |
| Green LED Cathode| Ground       | GND        | Pin 38     |
| Red LED Anode    | Signal       | GPIO21     | Pin 27     |
| Red LED Cathode  | Ground       | GND        | Pin 38     |

> ⚠️ **Note**: Use voltage dividers (R1 = 2.2kΩ and R2 = 3.3kΩ) on AO lines to step down from 5V to ~3.3V for safe ADC readings.

---

## ⚙️ Setup Instructions

### 🔧 Hardware
- Connect components as listed above  
- Adjust **MQ7** potentiometer for DOUT = 1 at ~50 ppm CO  
- Calibrate **MQ135** for ~400 ppm CO₂ in clean air (R₀ ≈ 24.56)

### 💻 Software
- Install **Arduino IDE**  
- Add **Arduino-Pico core** for Raspberry Pi Pico W  
- Install `UniversalTelegramBot` from Arduino Library Manager  

### ⚙️ Configuration
Edit `src/AirQualityMonitorWithIAQI.ino` and update:
```cpp
#define WIFI_SSID     "your_wifi"
#define WPA_PASSWORD  "your_password"
#define BOT_TOKEN     "your_bot_token"
#define CHAT_ID       "your_chat_id"
#define API_KEY       "your_thingspeak_api_key"
