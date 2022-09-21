#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi
const char *ssid = "Hậu"; // Enter your WiFi name
const char *password = "1toichin";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "broker.emqx.io";
const char *topic = "esp8266/message";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);


void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
      Serial.print((char) payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");
}

void setup() {
  // Set software serial baud to 115200;
  Serial.begin(115200);
  // connecting to a WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network!");

  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);
  while (!client.connected()) {
    String client_id = String(WiFi.macAddress());

      if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
          Serial.println("Connected to Public MQTT Broker");
      } else {
          Serial.print("Failed to connect with MQTT Broker");
          Serial.print(client.state());
          delay(2000);
      }
  }
  
  client.publish(topic, "Hello! I am ESP8266");
  client.subscribe(topic);
}


void loop() {
  client.loop();
}
