/* TMP36 analog temperature sensor with Arduino example code. More info: https://www.makerguides.com */

// Define to which pin of the Arduino the output of the TMP36 is connected:
const int sensorPin = A0;

void setup(void)
{
  // Begin serial communication at a baud rate of 9600:
  Serial.begin(9600);
}

void loop(void)
{
  // Get a reading from the temperature sensor:
  int reading = analogRead(sensorPin);

  // Convert the reading into voltage:
  float voltage = reading * (5000 / 1024.0);

  // Convert the voltage into the temperature in Celsius:
  float temperature = (voltage - 500) / 10;

  // Print the temperature in the Serial Monitor:
  Serial.print(temperature);
  Serial.print(" \xC2\xB0"); // shows degree symbol
  Serial.println("C");

  delay(1000); // wait a second between readings
}
