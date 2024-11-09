import serial
import pynmea2

# Set up the serial connection (adjust the port if necessary)
gps_serial = serial.Serial('/dev/ttyTHS1', baudrate=9600, timeout=1)

while True:
    try:
        # Read a line from the GPS module
        line = gps_serial.readline().decode('utf-8', errors='ignore').strip()

        # Check if the line starts with a valid NMEA sentence
        if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
            # Parse the NMEA sentence
            msg = pynmea2.parse(line)

            # If it's a GGA sentence, it contains latitude/longitude info
            if isinstance(msg, pynmea2.GGA) or isinstance(msg, pynmea2.RMC):
                print(f"Latitude: {msg.latitude} {msg.lat_dir}")
                print(f"Longitude: {msg.longitude} {msg.lon_dir}")
                print(f"Timestamp: {msg.timestamp}")
    except pynmea2.ParseError as e:
        print(f"Parse error: {e}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")

        
