
class MegaHandler:
    def __init__(self, port, baud_rate=115200, timeout=1):
        """
        Initialization
        """
        
        self.serial_connection = serial.Serial(port, baud_rate, timeout=timeout)
        self.running = True 
        print(f"Connected to Mega on {port}")

    def read_serial(self):
        """
        Continuously read from the serial connection.
        """
        
        while self.running:
            if self.serial_connection.in_waiting > 0:
                line = self.serial_connection.readline().decode('utf-8').strip()
                print(f"Received: {line}")

    def stop(self):
        """
        Stops the thread and closes the serial connection.
        """

        self.running = False
        time.sleep(0.5)  
        self.serial_connection.close()
        print("Serial connection closed.")
