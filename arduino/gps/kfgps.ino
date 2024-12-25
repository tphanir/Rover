#include <TinyGPS++.h>
#include <SimpleKalmanFilter.h>
#include "BluetoothSerial.h"

// Define the RX and TX pins for Serial 2 (GPS Module)
#define RXD2 16
#define TXD2 17

#define GPS_BAUD 9600
unsigned long lastCheck = 0;

// Initialize HardwareSerial for GPS communication
HardwareSerial gpsSerial(2);
TinyGPSPlus gps;
BluetoothSerial SerialBT;

// Initialize Kalman Filters for Latitude and Longitude
// Parameters: (processNoise, measurementNoise, estimatedError)
SimpleKalmanFilter kalmanLat(1e-5, 1e-2, 1);
SimpleKalmanFilter kalmanLon(1e-5, 1e-2, 1);

// Variables to store filtered data
double filteredLat = 0.0;
double filteredLon = 0.0;

// Buffer for multiple readings
const int BUFFER_SIZE = 20; // Number of readings to store
double latBuffer[BUFFER_SIZE];
double lonBuffer[BUFFER_SIZE];
int bufferIndex = 0;
bool bufferFilled = false;

// Configuration parameters
const int REQUIRED_SATELLITES = 6; // Minimum satellites for a reliable fix
const double MAX_HDOP = 2.0;       // Maximum HDOP for acceptable accuracy

void setup(){
  Serial.begin(115200);
  gpsSerial.begin(GPS_BAUD, SERIAL_8N1, RXD2, TXD2);
  SerialBT.begin("HiPhani");
  Serial.println("Initializing GPS with SimpleKalmanFilter and Averaging...");
  
  // Initialize buffer with zeros
  for(int i = 0; i < BUFFER_SIZE; i++){
    latBuffer[i] = 0.0;
    lonBuffer[i] = 0.0;
  }
  
  // Configure GPS to 5 Hz
  setGPSUpdateRate(200); // 200 ms corresponds to 5 Hz
  delay(1000); // Wait for GPS module to process the configuration
}

// Function to set GPS update rate via UBX-RATE message
void setGPSUpdateRate(uint16_t measurementRate) {
  // UBX-RATE message structure for measurementRate
  uint8_t ubxRate[20] = {
    0xB5, 0x62,       // Header
    0x06, 0x08,       // Class, ID
    0x06, 0x00,       // Length (6 bytes payload)
    0xC8, 0x00, 0x00, 0x00, // Measurement Rate (200 ms)
    0x01, 0x00, 0x00, 0x00, // Navigation Rate (1)
    0x00, 0x00, 0x00, 0x00, // Time Reference (UTC)
    0x00, 0x00        // Checksum (to be calculated)
  };

  // Update measurementRate in payload
  ubxRate[6] = measurementRate & 0xFF;         // LSB
  ubxRate[7] = (measurementRate >> 8) & 0xFF;  // MSB

  // Calculate checksum
  uint8_t CK_A = 0;
  uint8_t CK_B = 0;
  for(int i = 2; i < 18; i++) { // From Class to last payload byte
    CK_A = CK_A + ubxRate[i];
    CK_B = CK_B + CK_A;
  }
  ubxRate[18] = CK_A;
  ubxRate[19] = CK_B;

  // Send UBX-RATE message to GPS
  gpsSerial.write(ubxRate, 20);
  Serial.println("UBX-RATE message sent to GPS module.");
}

// Function to calculate median
double calculateMedian(double *buffer, int size){
  // Create a copy of the buffer to sort
  double temp[size];
  for(int i = 0; i < size; i++) temp[i] = buffer[i];
  
  // Simple Bubble Sort
  for(int i = 0; i < size-1; i++){
    for(int j = 0; j < size-i-1; j++){
      if(temp[j] > temp[j+1]){
        double swap = temp[j];
        temp[j] = temp[j+1];
        temp[j+1] = swap;
      }
    }
  }
  
  // Return the middle element
  if(size % 2 == 0){
    return (temp[size/2 - 1] + temp[size/2]) / 2.0;
  }
  else{
    return temp[size/2];
  }
}

void loop(){
  // Read data from GPS
  while (gpsSerial.available() > 0){
    char c = gpsSerial.read();
    if (gps.encode(c)){
      // Check for a valid fix with sufficient satellites and acceptable HDOP
      if (gps.location.isValid() && 
          gps.satellites.value() >= REQUIRED_SATELLITES && 
          gps.hdop.hdop() < MAX_HDOP){
        
        double currentLat = gps.location.lat();
        double currentLon = gps.location.lng();
        
        // Apply Kalman Filter to the current readings
        filteredLat = kalmanLat.updateEstimate(currentLat);
        filteredLon = kalmanLon.updateEstimate(currentLon);
        
        // Store filtered readings into the buffer
        latBuffer[bufferIndex] = filteredLat;
        lonBuffer[bufferIndex] = filteredLon;
        bufferIndex++;
        
        // Check if buffer is filled
        if(bufferIndex >= BUFFER_SIZE){
          bufferIndex = 0;
          bufferFilled = true;
        }
        
        // If buffer is filled, calculate the average and median
        if(bufferFilled){
          // Simple Averaging
          double sumLat = 0.0;
          double sumLon = 0.0;
          
          for(int i = 0; i < BUFFER_SIZE; i++){
            sumLat += latBuffer[i];
            sumLon += lonBuffer[i];
          }
          
          double avgLat = sumLat / BUFFER_SIZE;
          double avgLon = sumLon / BUFFER_SIZE;
          
          // Output the averaged coordinates
          SerialBT.print("Accurate Latitude (Average): ");
          SerialBT.println(avgLat, 6);
          SerialBT.print("Accurate Longitude (Average): ");
          SerialBT.println(avgLon, 6);
          SerialBT.print("HDOP: ");
          SerialBT.println(gps.hdop.hdop());
          SerialBT.print("Satellites: ");
          SerialBT.println(gps.satellites.value());
          SerialBT.println("---------------------------");
          
          // Optional: Calculate and output Median
          double medianLat = calculateMedian(latBuffer, BUFFER_SIZE);
          double medianLon = calculateMedian(lonBuffer, BUFFER_SIZE);
          
          SerialBT.print("Accurate Latitude (Median): ");
          SerialBT.println(medianLat, 6);
          SerialBT.print("Accurate Longitude (Median): ");
          SerialBT.println(medianLon, 6);
          SerialBT.println("===========================");
        }
      }
    }
  }
}
