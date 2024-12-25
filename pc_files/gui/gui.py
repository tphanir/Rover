import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import serial
import time
import threading

ser = None  # Global variable to hold serial connection
autonomous_active = False  # Flag to track if autonomous mode is active
manual_active = False  # Flag to track if manual mode is active

def open_serial():
    global ser
    try:
        port = '/dev/ttyUSB0' 
        ser = serial.Serial(port, 57600, timeout=1)
        print("Serial connection opened.")
        ser.flush()
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    return ser

def close_serial():
    global ser
    if ser and ser.is_open:
        ser.close()
        print("Serial connection closed.")
    ser = None

def send_mode_message(mode):
    """Send the active mode (Manual or Autonomous) to the serial port."""
    if ser and ser.is_open:
        ser.write(mode.encode('utf-8') + b'\n')
        print(f"Sent Mode: {mode}")
        
def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()
    main_menu()

def main_menu():
    # Set the background
    #bg_label = tk.Label(root, image=bg_image)
    #bg_label.place(relwidth=1, relheight=1)

    # Add title "Genesis"
    title_label = tk.Label(
        root,
        text="Genesis",
        font=("Helvetica", 40, "bold"),
        bg="#ffffff",
        fg="#000000"
    )
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    # Buttons for Manual and Autonomous
    manual_button = tk.Button(
        root,
        text="Manual",
        font=("Helvetica", 20),
        command=lambda: manual_mode(),
        bg="#007BFF",
        fg="#FFFFFF",
        width=15,
        height=2
    )
    manual_button.place(relx=0.3, rely=0.5, anchor="center")

    autonomous_button = tk.Button(
        root,
        text="Autonomous",
        font=("Helvetica", 20),
        command=lambda: autonomous_mode(),
        bg="#28A745",
        fg="#FFFFFF",
        width=15,
        height=2
    )
    autonomous_button.place(relx=0.7, rely=0.5, anchor="center")

def autonomous_mode():
    global ser, autonomous_active, manual_active
    # Stop manual mode if it's active
    if manual_active:
        manual_active = False
        close_serial()

    # Open serial port for communication if not already open
    if ser is None or not ser.is_open:
        ser = open_serial()

    autonomous_active = True  # Set the flag to true, indicating autonomous mode is active
    
    # Send the mode (Autonomous)
    send_mode_message("Autonomous")

    for widget in root.winfo_children():
        widget.destroy()

    entry_label = tk.Label(
        root,
        text="Enter Target GPS Coordinates:",
        font=("Helvetica", 16),
        bg="#ffffff",
        fg="#000000"
    )
    entry_label.pack(pady=20)

    gps_entry = tk.Entry(root, font=("Helvetica", 14))
    gps_entry.pack(pady=10)

    def submit_coordinates():
        global autonomous_active
        gps_coordinates = gps_entry.get()  # Get the coordinates from the input field
        if gps_coordinates:
            print(f"Sending GPS Coordinates: {gps_coordinates}")
            ser.write(gps_coordinates.encode('utf-8') + b'\n')  # Send the coordinates once
            gps_entry.delete(0, tk.END)  # Clear the entry after submission

    # Bind Enter key to trigger submit_coordinates
    def on_enter_key(event):
        submit_coordinates()

    root.bind("<Return>", on_enter_key)  # Bind Enter key to submit_coordinates

    submit_button = tk.Button(
        root,
        text="Submit",
        font=("Helvetica", 14),
        command=submit_coordinates,
        bg="#28A745",
        fg="#FFFFFF"
    )
    submit_button.pack(pady=20)

    def back_to_menu():
        global autonomous_active
        autonomous_active = False  # Stop autonomous mode when going back to menu
        ser.write("stop".encode('utf-8') + b'\n')  # Send key over serial
        close_serial()
        show_main_menu()

    back_button = tk.Button(
        root,
        text="Back",
        font=("Helvetica", 14),
        command=back_to_menu,
        bg="#DC3545",
        fg="#FFFFFF"
    )
    back_button.pack(pady=20)

    # Bind 'B' key for back action
    def on_b_key(event):
        back_to_menu()

    root.bind("b", on_b_key)  # Bind B key to back_to_menu

def manual_mode():
    global ser, manual_active, autonomous_active
    # Stop autonomous mode if it's active
    if autonomous_active:
        autonomous_active = False
        close_serial()

    # Open serial port for communication if not already open
    if ser is None or not ser.is_open:
        ser = open_serial()

    manual_active = True  # Set the flag to true, indicating manual mode is active
    
    # Send the mode (Manual)
    send_mode_message("Manual")

    for widget in root.winfo_children():
        widget.destroy()

    manual_label = tk.Label(
        root,
        text="Manual Mode (WASD Keys to Move):",
        font=("Helvetica", 16),
        bg="#ffffff",
        fg="#000000"
    )
    manual_label.pack(pady=20)

    button_label = tk.Label(
        root,
        text="Button Pressed:",
        font=("Helvetica", 14),
        bg="#ffffff",
        fg="#000000"
    )
    button_label.pack()

    button_pressed = tk.StringVar()
    button_display = tk.Label(
        root,
        textvariable=button_pressed,
        font=("Helvetica", 20),
        bg="#ffffff",
        fg="#007BFF"
    )
    button_display.pack(pady=10)

    pressed_keys = set()  # To track which keys are being pressed
    
    def key_pressed(event):
        key = event.char.upper()
        if key in ['W', 'A', 'S', 'D', 'X']:
            pressed_keys.add(key)
            button_pressed.set(" ".join(sorted(pressed_keys)))
            # Send the corresponding key via serial
            ser.write(key.encode('utf-8') + b'\n')  # Send key over serial

    def key_released(event):
        key = event.char.upper()
        if key in ['W', 'A', 'S', 'D']:
            pressed_keys.discard(key)
            button_pressed.set(" ".join(sorted(pressed_keys)))

    def back_to_menu():
        global manual_active
        root.unbind("<KeyPress>")
        root.unbind("<KeyRelease>")
        manual_active = False  # Stop manual mode when going back to menu
        ser.write("stop".encode('utf-8') + b'\n')  # Send key over serial
        close_serial()
        show_main_menu()

    root.bind("<KeyPress>", key_pressed)
    root.bind("<KeyRelease>", key_released)

    # Bind 'B' key for back action
    def on_b_key(event):

        back_to_menu()

    root.bind("b", on_b_key)  # Bind B key to back_to_menu

    back_button = tk.Button(
        root,
        text="Back",
        font=("Helvetica", 14),
        command=back_to_menu,
        bg="#DC3545",
        fg="#FFFFFF"
    )
    back_button.pack(pady=20)

# Main Application
root = tk.Tk()
root.title("Genesis")
root.geometry("800x600")

# Load background image
#rover_image = Image.open("./rover.png")  # Replace with the actual path
#rover_image = rover_image.resize((800, 600))  # Resize to match window
#bg_image = ImageTk.PhotoImage(rover_image)

# Bind the Escape key to close the application
root.bind("<Escape>", lambda event: root.quit())  # Escape key to exit

# Initial main menu
main_menu()
root.mainloop()
