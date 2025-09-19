#include <DHT.h>

#define DHTPIN 2     // DHT11 data pin connected to digital pin 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // Send only valid data
  if (!isnan(temperature) && !isnan(humidity)) {
    Serial.print(temperature);
    Serial.print(",");
    Serial.println(humidity);
  }

  delay(2000); // Wait 2 seconds before sending again
}