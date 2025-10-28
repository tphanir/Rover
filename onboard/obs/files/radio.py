import serial
import time

def initialize_serial(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Connected to {port} at {baudrate} baud.")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to {port}: {e}")
        return None

def relay_commands(input_serial, output_serial):
    try:
        while True:
            if input_serial.in_waiting > 0:
                # Read command from the Laptop via RF
                command = input_serial.readline().decode('utf-8').strip()
                print(f"radio: {command}")

                # Validate the command
                if command in ['f', 'b', 'l', 'r', 's']:
                    # Send the valid command to Arduino Mega
                    output_serial.write(f"{command}\n".encode('utf-8'))
                elif command == 'exit':
                    break
                else:
                    print(f"Invalid command received: {command}")
            
            time.sleep(0.1)  # Prevent excessive CPU usage

    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        input_serial.close()
        output_serial.close()
        print("Serial ports closed.")

if __name__ == "__main__":
    # Configure serial ports
    laptop_port = '/dev/ttyUSB0'  # Laptop connection via RF
    arduino_port = '/dev/ttyUSB2'  # Arduino Mega connection
    baudrate = 57600

    # Initialize serial connections
    laptop_serial = initialize_serial(laptop_port, baudrate)
    arduino_serial = initialize_serial(arduino_port, baudrate)

    # Ensure both serial connections are established
    if laptop_serial and arduino_serial:
        relay_commands(laptop_serial, arduino_serial)
    else:
        print("Failed to initialize one or both serial connections.")

