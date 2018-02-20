#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

#define USE_SERIAL Serial



//const char* ssid = "MCV";
//const char* password = "zzl2115int";
const char* ssid = "SCU-Student";
const char* password = "gosantaclara";


const char* myssid = "Chang";
const char* mypassword = "";

ESP8266WebServer server(80);

void handleRoot()
{
  server.send(200, "text/plain", "It connected");
}

void handleOther()
{ const char* host;
  WiFiClient client;

  Serial.print("Requesting url");
  String requestUrl = server.uri();


  requestUrl.remove(0,1);
  int i = requestUrl.indexOf('/');
  String domain = requestUrl.substring(0,i);
  host = domain.c_str();
  requestUrl.remove(0,i);

  Serial.print("Host: ");
  Serial.println(host);
  Serial.print("requestUrl:");
  Serial.println(requestUrl);

  while (!client.connect(host, 80))
  {
    Serial.println("connection failed, Trying again");
  }

  client.print(String("GET ") + requestUrl);

  client.print(String(" HTTP/1.1\r\n") +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");

  // check if it is timeout.
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 5000) {
      Serial.println(">>> Client Timeout !");
      client.stop();
      return;
    }
  }


  while(!client.available())
  {
    yield();
  }

  String line;
  while(client.available())
  {
    line = client.readStringUntil('\r');
    line.replace("HTTP", "WHAT-IS-THIS");
    line.replace("http", "WHAT-IS-THIS");
    Serial.print(line);
  }
  delay(4000);
  server.send(200, "text/htm", line);

  client.stop();
}

void setup(void)
{
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  WiFi.softAP(myssid, mypassword);
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(myIP);

  server.on("/", handleRoot);

  server.onNotFound(handleOther);

  server.begin();
  Serial.println("HTTP Server Started");
}

void loop(void){
  server.handleClient();
}