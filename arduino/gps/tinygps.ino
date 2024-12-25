#include <TinyGPS++.h>
#include <BluetoothSerial.h>

// Check if Bluetooth is available (ESP32)
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// Define the RX and TX pins for Serial 2 (GPS Module)
#define RXD2 16
#define TXD2 17

#define GPS_BAUD 9600

// Create a TinyGPS++ object
TinyGPSPlus gps;

// Create an instance of the HardwareSerial class for Serial 2
HardwareSerial gpsSerial(2);

// Create a BluetoothSerial object
BluetoothSerial SerialBT;

// Variable to store incoming Bluetooth data
String btInput = "";

void setup() {
  // Initialize Serial Monitor for debugging
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for Serial Monitor to open (optional)
  }
  Serial.println("Starting GPS and Bluetooth Module...");

  // Start Serial 2 for GPS communication
  gpsSerial.begin(GPS_BAUD, SERIAL_8N1, RXD2, TXD2);
  Serial.println("GPS Serial (Serial2) started at 9600 baud rate");

  // Initialize Bluetooth Serial with a device name
  if (!SerialBT.begin("ESP32_GPS_BT")) { // You can change "ESP32_GPS_BT" to your desired name
    Serial.println("An error occurred initializing Bluetooth");
  } else {
    Serial.println("Bluetooth initialized successfully");
  }

  Serial.println("Setup complete. Waiting for commands...");
}

void loop() {
  // Process GPS data for 1 second
  unsigned long start = millis();

  while (millis() - start < 1000) {
    while (gpsSerial.available() > 0) {
      char c = gpsSerial.read();
      gps.encode(c);
    }
  }

  // Check if new GPS location data is available
  if (gps.location.isUpdated()) {
    // Optionally, you can print GPS data to Serial Monitor
    Serial.println("New GPS data received:");
    Serial.print("LAT: ");
    Serial.println(gps.location.lat(), 6);
    Serial.print("LONG: "); 
    Serial.println(gps.location.lng(), 6);
    Serial.print("SPEED (km/h) = "); 
    Serial.println(gps.speed.kmph()); 
    Serial.print("ALT (meters) = "); 
    Serial.println(gps.altitude.meters());
    Serial.print("HDOP = "); 
    Serial.println(gps.hdop.value() / 100.0); 
    Serial.print("Satellites = "); 
    Serial.println(gps.satellites.value()); 
    Serial.print("Time in UTC: ");
    Serial.println(String(gps.date.year()) + "/" + String(gps.date.month()) + "/" + String(gps.date.day()) + "," + String(gps.time.hour()) + ":" + String(gps.time.minute()) + ":" + String(gps.time.second()));
    Serial.println("");
  }

  // Handle Bluetooth communication
  while (SerialBT.available()) {
    char incomingChar = SerialBT.read();
    if (incomingChar == '\n' || incomingChar == '\r') {
      // End of command
      btInput.trim(); // Remove any leading/trailing whitespace
      if (btInput.equalsIgnoreCase("GIVE")) {
        sendGPSDataOverBluetooth();
      }
      btInput = ""; // Reset for the next command
    } else {
      btInput += incomingChar;
    }
  }

  // Optional: Add a small delay to prevent overwhelming the loop
  delay(10);
}

// Function to send GPS data over Bluetooth
void sendGPSDataOverBluetooth() {
  if (gps.location.isValid()) {
    String gpsData = "LAT: " + String(gps.location.lat(), 6) + "\n" +
                     "LONG: " + String(gps.location.lng(), 6) + "\n" +
                     "SPEED (km/h): " + String(gps.speed.kmph()) + "\n" +
                     "ALT (meters): " + String(gps.altitude.meters()) + "\n" +
                     "HDOP: " + String(gps.hdop.value() / 100.0) + "\n" +
                     "Satellites: " + String(gps.satellites.value()) + "\n" +
                     "Time UTC: " + String(gps.date.year()) + "/" + String(gps.date.month()) + "/" + String(gps.date.day()) +
                     "," + String(gps.time.hour()) + ":" + String(gps.time.minute()) + ":" + String(gps.time.second()) + "\n";

    SerialBT.println(gpsData);
    Serial.println("GPS data sent over Bluetooth.");
  } else {
    SerialBT.println("GPS data not available.");
    Serial.println("GPS data not available to send.");
  }
}
