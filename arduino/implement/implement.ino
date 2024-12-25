#include "math.h"
#include "compass.h"
#include "motor.h"
#include "QMC5883LCompass.h"
#include <TinyGPS++.h>
#include "BluetoothSerial.h"

#define RXD2 16
#define TXD2 17
#define GPS_BAUD 9600

const double HEADING_ERROR = 5.0;
const double PROXIMITY = 1.0;

const int NUM_OF_POINTS = 8;

double coordinates[8][2] = {
    {21.123465, 79.049529},
    {21.123363, 79.049628},
    {21.123239, 79.049568},
    {21.123186, 79.049477},
    {21.123075, 79.049562},
    {21.123168, 79.049665},
    {21.123127, 79.049842},
    {21.123078, 79.050077}
};

HardwareSerial gpsSerial(2);
BluetoothSerial SerialBT;
QMC5883LCompass compass;
TinyGPSPlus gps;

double distance, heading;
double  lat1 = 0,
        lon1 = 0, 
        lat2 = 0,
        lon2 = 0;

double azimuthAngle = 0.0;
boolean done = true;

String btInput = "";
bool stringComplete = false;
long past;

int i = -1;

void updateLocation() {
  if (gps.location.isUpdated()) {
    lat1 = gps.location.lat();
    lon1 = gps.location.lng();
  }
}

void updateAzimuth() {
  compass.read();
  azimuthAngle = compass.getAzimuth();
}

void move(double angle) {
  double error = azimuthAngle - angle;

  if(abs(error) < HEADING_ERROR) {
    forward();
  }
  else {
    if(error > 0.0) {
      left();
    } else {
      right();
    }
    delay(500);
  }
}


void go() {
  if(done) {
    if(millis() - past > 5000) {
      SerialBT.println("C:  " + String(lat1, 6) + ", " + String(lon1, 6));
      SerialBT.println("T:  " + String(lat2, 6) + ", " + String(lon2, 6));
      past = millis();
    }
    return;
  }
  
  distance = haversine(lat1, lon1, lat2, lon2);
  heading = bearing(lat1, lon1, lat2, lon2);
  
  if(millis() - past > 2000) {
    SerialBT.println("C:  " + String(lat1, 6) + ", " + String(lon1, 6));
    SerialBT.println("T:  " + String(lat2, 6) + ", " + String(lon2, 6));

    double normalizedAzimuth = azimuthAngle;
    if(normalizedAzimuth < 0) normalizedAzimuth += 360;
    
    SerialBT.println("D: " + String(distance) +
                     " H: " + String(heading) +
                     " A: " + String(normalizedAzimuth)
    );
    SerialBT.println();
    past = millis();
  }


  if(distance > PROXIMITY && distance < 500) {
    heading = bearing(lat1, lon1, lat2, lon2);
    if(heading > 180) {
      heading -= 360;
    }
    move(heading);
  } else if(distance < PROXIMITY){
    berhenti();
    Serial.println("Point Reached");
    done = true;
    lat2 = 0;
    lon2 = 0;
    delay(10000);
  } else {
    berhenti();
  }
}

void setup() {
  Serial.begin(115200);
  gpsSerial.begin(GPS_BAUD, SERIAL_8N1, RXD2, TXD2);

  SerialBT.begin("ESP");
  setup_motor();
  delay(1000);
  
  compass.init();
  compass.setMode(qmc5883l_mode_cont, qmc5883l_odr_10hz, qmc5883l_rng_8g, qmc5883l_osr_512);
  past = millis();
}

void loop() {
  while (gpsSerial.available() > 0) {
    gps.encode(gpsSerial.read());
  }

  while (SerialBT.available()) {
    char incomingChar = SerialBT.read();
    if (incomingChar == '\n') {
      stringComplete = true;
    } else {
      btInput += incomingChar;
    }
  }

  if(stringComplete) {
    int spaceIndex = btInput.indexOf(' ');
    if (spaceIndex != -1) {
      String command = btInput.substring(0, spaceIndex);
      String valueStr = btInput.substring(spaceIndex + 1);

      if (command.equalsIgnoreCase("go")) {
        int index = valueStr.toInt(); // Convert to integer
        if(index < NUM_OF_POINTS) {
            i = index;
            lat2 = coordinates[index][0];
            lon2 = coordinates[index][1];
            SerialBT.println("Navigating to point " + String(i));
            done = false;
            delay(5000);
        } else {
          // index out of range.
        }
      } else if (command.equalsIgnoreCase("stop")){
        lat2 = lon2 = 0;
        done = true;
        berhenti();
      }
    } else {
      // invalid format
    }

    btInput = "";
    stringComplete = false;
  }

  updateLocation();
  updateAzimuth();
  go();

  delay(10);
}  
