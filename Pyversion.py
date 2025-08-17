import time
import requests
import spidev
import RPi.GPIO as GPIO

# ======================
# Configurations
# ======================

# Telegram Bot credentials
BOT_TOKEN = "your_bot_token"
CHAT_ID = "your_chat_id"

# ThingSpeak
API_KEY = "your_thingspeak_api_key"
CHANNEL_ID = 123456  # Replace with your actual ThingSpeak Channel ID

# GPIO pins
GREEN_LED = 19
RED_LED = 21
BUZZER = 18

# Thresholds (tune as per your calibration)
THRESHOLD = 600  

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# Setup SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0 (CE0)
spi.max_speed_hz = 1350000


# ======================
# Functions
# ======================

def read_adc(channel):
    """Read from MCP3008 ADC channel (0-7)"""
    if channel < 0 or channel > 7:
        return -1
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def send_to_thingspeak(mq137, mq7):
    """Send data to ThingSpeak"""
    url = "https://api.thingspeak.com/update"
    payload = {
        "api_key": API_KEY,
        "field1": mq137,
        "field2": mq7
    }
    try:
        response = requests.get(url, params=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Data pushed to ThingSpeak")
        else:
            print(f"❌ Push error: {response.status_code}")
    except Exception as e:
        print("⚠️ ThingSpeak error:", e)


def send_telegram_alert(mq137, mq7):
    """Send alert message via Telegram"""
    message = f"⚠️ ALERT! Poor air quality detected!\nMQ137: {mq137}\nMQ7: {mq7}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.status_code == 200:
            print("📩 Telegram alert sent")
        else:
            print(f"⚠️ Telegram error: {response.status_code}")
    except Exception as e:
        print("⚠️ Telegram send failed:", e)


def air_quality_monitor():
    print("🚀 Air Quality Monitor Started (MQ137 + MQ7 on Raspberry Pi)")

    try:
        while True:
            # Read values from ADC channels
            mq137Value = read_adc(0)  # connect MQ137 to MCP3008 CH0
            mq7Value = read_adc(1)    # connect MQ7 to MCP3008 CH1

            print(f"MQ137: {mq137Value}   MQ7: {mq7Value}")

            # Send data to ThingSpeak
            send_to_thingspeak(mq137Value, mq7Value)

            # Threshold alerts
            if mq137Value > THRESHOLD or mq7Value > THRESHOLD:
                GPIO.output(RED_LED, GPIO.HIGH)
                GPIO.output(GREEN_LED, GPIO.LOW)
                GPIO.output(BUZZER, GPIO.HIGH)
                print("🚨 ALERT! Poor air quality")
                send_telegram_alert(mq137Value, mq7Value)
            else:
                GPIO.output(GREEN_LED, GPIO.HIGH)
                GPIO.output(RED_LED, GPIO.LOW)
                GPIO.output(BUZZER, GPIO.LOW)
                print("✅ Air quality is good")

            time.sleep(20)  # 20s delay same as ESP32 code

    except KeyboardInterrupt:
        print("\n🛑 Program stopped by user")
    finally:
        GPIO.cleanup()
        spi.close()


# ======================
# Run
# ======================
if __name__ == "__main__":
    air_quality_monitor()
