
#include <WiFi.h>
#include <ThingSpeak.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>

// WiFi credentials
const char* WIFI_SSID = "your_wifi_ssid";
const char* WPA_PASSWORD = "your_wifi_password";

// Telegram Bot credentials
const char* BOT_TOKEN = "your_bot_token";
const char* CHAT_ID = "your_chat_id";

// ThingSpeak
const char* API_KEY = "your_thingspeak_api_key";
unsigned long channelID = 123456; // Replace with your actual ThingSpeak Channel ID

WiFiClientSecure client;
UniversalTelegramBot bot(BOT_TOKEN, client);

int mq135Pin = 35;
int mq7Pin = 34;
int greenLED = 19;
int redLED = 21;
int buzzer = 18;

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WPA_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void setup() {
  Serial.begin(115200);
  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(buzzer, OUTPUT);

  connectWiFi();
  client.setInsecure();  // Only for testing, remove for production
  ThingSpeak.begin(client);
}

void loop() {
  int mq135Value = analogRead(mq135Pin);
  int mq7Value = analogRead(mq7Pin);

  Serial.print("MQ135: ");
  Serial.print(mq135Value);
  Serial.print("  MQ7: ");
  Serial.println(mq7Value);

  ThingSpeak.setField(1, mq135Value);
  ThingSpeak.setField(2, mq7Value);

  int status = ThingSpeak.writeFields(channelID, API_KEY);
  if (status == 200) {
    Serial.println("Data pushed to ThingSpeak");
  } else {
    Serial.println("Push error: " + String(status));
  }

  // Threshold alerts
  if (mq135Value > 600 || mq7Value > 600) {
    digitalWrite(redLED, HIGH);
    digitalWrite(greenLED, LOW);
    digitalWrite(buzzer, HIGH);

    String alertMsg = "⚠️ ALERT! Poor air quality detected!\n";
    alertMsg += "MQ135: " + String(mq135Value) + "\n";
    alertMsg += "MQ7: " + String(mq7Value);
    bot.sendMessage(CHAT_ID, alertMsg, "");
  } else {
    digitalWrite(greenLED, HIGH);
    digitalWrite(redLED, LOW);
    digitalWrite(buzzer, LOW);
  }

  delay(20000);  // Wait before sending next update
}
