import numpy as np
import cv2
import time
import threading
import re
import subprocess
import pyrealsense2 as rs
import os

from handlers.serial import SerialHandler
from handlers.manual import manual
from handlers.voice import voice

from controls.semiauto import semiauto
from controls.fullauto import fullauto

from helpers.forward import forward


def main():
    # Define serial connections
    radio = SerialHandler(port='/dev/ttyUSB0', baud_rate=57600, timeout=1)
    mega = SerialHandler(port='/dev/ttyACM0', baud_rate=115200, timeout=1)

    time.sleep(10)

    radio.open()
    mega.open()
    
    if mega.is_open and radio.is_open:
        thread = threading.Thread(target=forward, args=(mega, radio, ), daemon=True)
        thread.start()

    try:
        while True:    
            if radio.serial_connection and radio.serial_connection.in_waiting > 0:
                data = radio.serial_connection.readline().decode('utf-8').strip()

                print(f'[RECVD] {data}')
                
                if data == 'Manual':
                    mega.write("Manual\n".encode())
                    manual(radio, mega)

                elif data == 'Semi-Autonomous':
                    mega.write("Semi-Autonomous\n".encode())
                    semiauto(radio, mega)

                elif data == 'Full-Autonomous':
                    mega.write("Full-Autonomous\n".encode())
                    fullauto(radio, mega)

                elif data == "Do-Calibration":
                    mega.write("Do-Calibration\n".encode())

                elif data == 'Set-Coordinates':
                    mega.write("Set-Coordinates\n".encode())
                    gps(radio, mega)

                elif data == "GPS-Only":
                    mega.write("GPS-Only\n".encode())

                elif data == "Voice-Nav":
                    voice(radio, mega)


                elif data == 'return':
                    data = "return\n"
                    mega.write(data.encode())
    except:
        print("\nExiting")
        mega.close()
        radio.close()
        thread.join()

if __name__ == "__main__":
    main()



    
