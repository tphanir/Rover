# Rover Genesis 

**Genesis** is a semi-autonomous rover platform designed for exploration, obstacle avoidance, and voice-controlled navigation. The system is split into two main components: the **Onboard** system (Jetson Nano + Arduino Mega) and the **Base Station** (Control Laptop).

## 📂 Project Structure

- **`base_station/`**: The ground control software. Features a Python/Tkinter GUI for sending commands (Manual, Auto, GPS) and viewing status.
- **`onboard/`**: The brain of the rover. Runs on an Nvidia Jetson Nano. Handles computer vision (RealSense), decision making, and serial communication with the Arduino.
- **`extra/`**: Experimental modules for IMU visualization, isolated CV tests, and serial debugging.
- **`pcb/`**: Custom PCB designs, schematics, and Gerber files for the rover's power and control distribution.
- **`docs/`**: Detailed hardware specs, media, and contributor descriptions.

## Getting Started

### Prerequisites
* **Hardware:** Nvidia Jetson Nano, Arduino Mega, Intel RealSense Depth Camera, Radio Modules.
* **Software:** Python 3.6+, OpenCV, PyRealSense2, Tkinter.

### Installation
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/IvLabs/Rover.git](https://github.com/IvLabs/Rover.git)
    ```
2.  **Setup Onboard (Jetson):**
    Navigate to `onboard/` and install dependencies (see `onboard/README.md`).
3.  **Setup Base Station:**
    Navigate to `base_station/` and run the GUI (see `base_station/README.md`).

## Contributors
* Aiden Ross D'souza
* Telukunta Phani Raj
* Koyaneni Yashwant
* Shubham Pandere
* Yuvraj Gupta