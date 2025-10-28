import serial  
import time

class SerialHandler:
    def __init__(self, port, baud_rate=57600, timeout=1):
        """
        Initialize a serial port connection.

        Args:
            port (str): The serial port (e.g., '/dev/ttyACM0').
            baud_rate (int): The baud rate for the serial communication.
            timeout (float): Timeout for read operations, in seconds.
        """
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.serial_connection = None

    def open(self):
        """
        Open the serial connection.
        """
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            print(f"[INFO] Serial connection opened on {self.port} at {self.baud_rate} baud.")
            #self.write(f'[INFO] Serial Radio connection established on {self.port} at {self.baud_rate} baud.\n')
        except serial.SerialException as e:
            print(f"[ERROR] Failed to open serial port {self.port}:\n{e}")

    def close(self):
        """
        Close the serial connection.
        """
        if self.serial_connection and self.serial_connection.is_open:
            print(f"[INFO] Serial connection on {self.port} closed.")
            #self.write(f'[INFO] Radio connection on {self.port} closed.\n')
            self.serial_connection.close()
        else:
            print(f"[WARNING] Serial connection on {self.port} is already closed.")

    def write(self, data):
        """
        Write data to the serial port.
        """
        if self.serial_connection and self.serial_connection.is_open:
            if isinstance(data, str):
                data = data.encode()  # Convert string to bytes
            self.serial_connection.write(data)
            print(f"[INFO] Sent data: {data}")
        else:
            print(f"[ERROR] Serial connection on {self.port} is not open.")
        time.sleep(0.25)

    def is_open(self):
        """
        Check if the serial connection is open.

        Returns:
            bool: True if the serial connection is open, False otherwise.
        """
        return self.serial_connection and self.serial_connection.is_open

