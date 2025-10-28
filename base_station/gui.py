import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from PIL import Image, ImageTk
import serial
from serial.tools import list_ports
import time

# Constants for Styling
TITLE_FONT = ("Segoe UI", 36, "bold") 
LABEL_FONT = ("Segoe UI", 14) 
BG_COLOR = "#2C3E50"
FG_COLOR = "#FFFFFF"


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


class CircularButton:
    def __init__(self, mode_frame, row, col, bg):
         # Manual Mode Button
        self.button = tk.Canvas(mode_frame, width=150, height=150, bg=bg, highlightthickness=0)
        self.button.grid(row=row, column=col, padx=30)
        
    def set(self, text, size, fill):
        self.button.create_oval(10, 10, 120, 120, fill=fill, outline="")
        self.text = self.button.create_text(65, 65, text=text, fill=FG_COLOR, font=("Segoe UI", size, "bold"))

    def bind(self, handler):
        self.handler = handler
        self.button.tag_bind(self.text, "<Button-1>", lambda e: self.handler())

class GenesisGUI:
    def __init__(self, root):
        self.root = root
        self.selected_port = tk.StringVar()
        self.motion_var = tk.StringVar(value="No motion detected")
        self.current_motion = None
        self.in_home_menu = True
        self.radio = None

        self.root.title("Genesis Control Panel")
        self.root.geometry("900x900")  # Increased window size
        self.root.configure(bg=BG_COLOR)
        self.create_widgets()
        
        # Bind Esc key to exit the application
        self.root.bind("<Escape>", self.exit_application)

    def create_widgets(self):
        """Create all widgets in the GUI."""
        self.clear_window()
        self.in_home_menu = True

        # Title
        title = tk.Label(self.root, text="Genesis Control", font=TITLE_FONT, fg=FG_COLOR, bg=BG_COLOR)
        title.pack(pady=30)

        # Serial Port Selection
        port_frame = tk.Frame(self.root, bg=BG_COLOR)
        port_frame.pack(pady=30)
        tk.Label(port_frame, text="Select Serial Port:", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR).pack(side=tk.LEFT, padx=10)
        self.port_dropdown = ttk.Combobox(port_frame, textvariable=self.selected_port, state="readonly", width=40)
        self.port_dropdown.pack(side=tk.LEFT, padx=20)
        ttk.Button(port_frame, text="Refresh", command=self.refresh_ports).pack(side=tk.LEFT, padx=10)
        self.refresh_ports()

        # Mode Selection Buttons
        mode_frame = tk.Frame(self.root, bg=BG_COLOR)
        mode_frame.pack(pady=50)

        # Manual Mode Button
        manual = CircularButton(mode_frame, 0, 0, BG_COLOR)
        manual.set("Manual", 14, "#28A745")
        manual.bind(self.manualHandler)

        # Autonomous Mode Button
        auto = CircularButton(mode_frame, 0, 1, BG_COLOR)
        auto.set("Auto", 14, "#007BFF")
        auto.bind(self.autoHandler)

        # Voice Mode Button
        voice = CircularButton(mode_frame, 1, 0, BG_COLOR)
        voice.set("Voice", 14, "#007BFF")
        voice.bind(self.voiceHandler)

        # Stream Mode Button
        stream = CircularButton(mode_frame, 1, 1, BG_COLOR)
        stream.set("Stream", 14, "#28A745")
        stream.bind(self.streamHandler)

         # Status Bar
        self.status_var = tk.StringVar(value="Status: Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR, anchor="w", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Start polling serial data
        #self.poll_serial_data()

    def refresh_ports(self):
        """Refresh the list of available serial ports."""
        ports = list_ports.comports()
        serial_ports = [port.device for port in ports if port.description.lower() != 'n/a']
        self.port_dropdown['values'] = serial_ports
        self.selected_port.set(serial_ports[0] if serial_ports else "")
        self.radio = SerialHandler(self.selected_port.get())

    def manualHandler(self):
        """Activate manual mode."""
        self.radio.open()
        self.radio.write("Manual\n")
        self.in_home_menu = False
        
        self.clear_window()

        # Instructions
        label = tk.Label(self.root, text="Use W, A, S, D, X for movement. Press B to go back.", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        label.pack(pady=30)

        # Motion Status
        motion_status = tk.Label(self.root, textvariable=self.motion_var, font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        motion_status.pack(pady=30)

        # Bind keypress and keyrelease events
        self.root.bind("<KeyRelease>", self.handle_keyrelease)
        self.root.bind("<KeyPress>", self.handle_keypress)

    
    def autoHandler(self):
        """Activate autonomous mode."""
        self.radio.open()
        self.clear_window()

        label = tk.Label(self.root, text="Select Navigation Mode", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        label.pack(pady=30)

        # Mode Selection Buttons
        mode_frame = tk.Frame(self.root, bg=BG_COLOR)
        mode_frame.pack(pady=50)

        # Buttons for GPS and Non-GPS options
        gps = CircularButton(mode_frame, 0, 0, BG_COLOR)
        gps.set("With GPS", 10, "#28A745")
        gps.bind(self.gpsHandler)

        # Buttons for GPS and Non-GPS options
        nogps = CircularButton(mode_frame, 0, 1, BG_COLOR)
        nogps.set("Without GPS", 10, "#28A745")
        nogps.bind(self.nogpsHandler)


    def voiceHandler(self):

        self.radio.open()
        self.radio.write("Voice-Nav\n")
        self.clear_window()

        # Instructions
        label = tk.Label(self.root, text="Voice Navigation Activated", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        label.pack(pady=30)

        # Bind keypress and keyrelease events
        self.root.bind("<KeyRelease>", self.handle_keyrelease)
        self.root.bind("<KeyPress>", self.handle_keypress)


    def streamHandler(self):

        self.radio.write("Live-Stream\n")
        self.clear_window()

        # Instructions
        label = tk.Label(self.root, text="Live Detection Stream", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        label.pack(pady=30)

        # Bind keypress and keyrelease events
        self.root.bind("<KeyRelease>", self.handle_keyrelease)
        self.root.bind("<KeyPress>", self.handle_keypress)

    def gpsHandler(self):
        """Menu for GPS-based navigation."""
        self.clear_window()

        instructions = tk.Label(self.root, text="GPS Navigation", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        instructions.pack(pady=20)

        # Buttons for Set and Go
        set_button = ttk.Button(self.root, text="Set Coordinates", command=self.set_coordinates)
        set_button.pack(pady=20)

        calibrate_button = ttk.Button(self.root, text="Calibrate", command=self.calibrate_func)
        calibrate_button.pack(pady=20)

        auto_button = ttk.Button(self.root, text="Go (GPS + O.A.)", command=self.send_go_auto_message)
        auto_button.pack(pady=20)

        gps_button = ttk.Button(self.root, text="Go (only GPS)", command=self.send_go_gps_message)
        gps_button.pack(pady=20)

        # Bind keypress and keyrelease events

        self.root.bind("<KeyRelease>", self.handle_keyrelease)
        self.root.bind("<KeyPress>", self.handle_keypress)



    def set_coordinates(self):
        """Set target GPS coordinates."""
        
        self.clear_window()
        self.radio.write("Set-Coordinates\n")

        instructions = tk.Label(self.root, text="Enter Target GPS Coordinates", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        instructions.pack(pady=20)

        self.gps_entry = tk.Entry(self.root, font=LABEL_FONT)
        self.gps_entry.pack(pady=10)

        set_button = ttk.Button(self.root, text="Set", command=self.store_coordinates)
        set_button.pack(pady=20)
        
        self.root.bind("<KeyPress>", self.handle_keypress)


    def store_coordinates(self):
        """Store and display target GPS coordinates."""
        self.target_coordinates = self.gps_entry.get()  # Store the coordinates
        if not self.target_coordinates:
            messagebox.showerror("Error", "Please enter valid GPS coordinates.")
            return

        self.radio.write(f"gps {self.target_coordinates}\n")
        
        self.clear_window()
        instructions = tk.Label(self.root, text=f"Target Coordinates Set: {self.target_coordinates}", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        instructions.pack(pady=20)

        auto_button = ttk.Button(self.root, text="Go (GPS + O.A.)", command=self.send_go_auto_message)
        auto_button.pack(pady=20)

        gps_button = ttk.Button(self.root, text="Go (only GPS)", command=self.send_go_gps_message)
        gps_button.pack(pady=20)

    def send_go_auto_message(self):
        """Send the 'Go' message with the target coordinates."""
        if hasattr(self, "target_coordinates") and self.target_coordinates:
            self.radio.write(f"Full-Autonomous\n")
            
            messagebox.showinfo("Message Sent", f"Sent GO command with coordinates: {self.target_coordinates}")
            self.clear_window()
            instructions = tk.Label(self.root, text="Auto GPS Activated", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        
            instructions.pack(pady=20)
        else:
            messagebox.showerror("Error", "Target coordinates not set.")


    def calibrate_func(self):
        self.radio.write("Do-Calibration\n")
        #messagebox.showinfo("Started Calibration")

            
    def send_go_gps_message(self):
        """Send the 'Go' message with the target coordinates."""
        if hasattr(self, "target_coordinates") and self.target_coordinates:
            self.radio.write('GPS-only\n')
            
            messagebox.showinfo("Message Sent", f"Sent GO command with coordinates: {self.target_coordinates}")
            self.clear_window()
            instructions = tk.Label(self.root, text="Auto GPS Activated", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        
            instructions.pack(pady=20)
        else:
            messagebox.showerror("Error", "Target coordinates not set.")

    def nogpsHandler(self):
        """Menu for non-GPS autonomous mode."""
        self.clear_window()

        instructions = tk.Label(self.root, text="Non-GPS Autonomous Navigation Started", font=LABEL_FONT, fg=FG_COLOR, bg=BG_COLOR)
        instructions.pack(pady=30)
        self.radio.write('Semi-Autonomous'.encode('utf-8') + b'\n')
        
        # Bind keypress and keyrelease events
        self.root.bind("<KeyPress>", self.handle_keypress)
        self.root.bind("<KeyRelease>", self.handle_keyrelease)

    def handle_keyrelease(self, event):
        key = event.char.upper()

        motions = {
            "W": "Moving Forward",
            "A": "Turning Left",
            "S": "Moving Backward",
            "D": "Turning Right",
            "X": "Stop",
            "B": "Returning to Main Menu",
        }
        if key in motions:
            self.motion_var.set("Stop")
            #self.radio.write('stop\n')

    def handle_keypress(self, event):
        """Handle keypress events for manual control."""
        key = event.char.upper()
        
        self.clicked = time.time()
        motions = {
            "W": "Moving Forward",
            "A": "Turning Left",
            "S": "Moving Backward",
            "D": "Turning Right",
            "X": "Stop",
            "B": "Returning to Main Menu",
        }
        
        if key in motions:
            if key == "B":
                if self.radio.is_open:
                    self.radio.write('return\n')
                
                self.back_to_menu()
                return

            if self.current_motion != key:
                self.current_motion = key
                self.motion_var.set(motions[key])
                self.radio.write(f'{key}\n')
                

    def back_to_menu(self):
        """Return to the main menu."""
        self.clear_window()
        if self.radio.is_open:
            self.radio.close()
        self.create_widgets()

        self.root.unbind("<KeyPress>")
        self.root.unbind("<KeyRelease>")
    
    def poll_serial_data(self):
        """Poll the serial port for incoming data."""
        if self.ser and self.ser.is_open:
            try:
                data = self.ser.readline().decode('utf-8').strip()
                if data:
                    self.status_var.set(f"Received: {data}")
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
        self.root.after(100, self.poll_serial_data)  # Poll every 100 ms


    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def exit_application(self, event=None):
        """Exit the application when Esc is pressed in the home menu."""
        if self.in_home_menu:
            self.root.quit()
        else:
            messagebox.showwarning("Exit Denied", "You can only exit from the home menu.")

    def run(self):
        """Run the GUI main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = GenesisGUI(root)
    app.run()


