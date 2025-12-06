# Extra / Experiments

This directory contains **miscellaneous experiments** and legacy code developed during the evolution of the **Rover** project.  
While not part of the main rover control system, these files served as important learning points for specific features, hardware integration, and testing.

---

## Overview

### `detection/`
- Contains multiple programs (`obstacle_x.py`) developed to test various Computer Vision (CV) methods for obstacle detection.
- **Requirement:** Intel RealSense camera.

### `imu/`
- Contains the IMU visualization and orientation tracking code (`imu.py`).
- Visualizes 3D motion of the rover (roll, pitch, yaw) using **PyOpenGL** and **pygame**.
- **Modes:**
  - **Connected:** Reads live orientation data from the ESP32-IMU.
  - **Disconnected:** Runs in simulation mode showing a static/rotating cube.

### `legacy/`
- Contains older versions of the main loop or scratchpad code (`main.py`) used for testing logic before integration into the `onboard` system.

### `serial/`
- Contains serial communication testing code (`radio.py`).
- Used to verify reading and relaying command data from the control computer (Base Station) via LoRa/Radio.

### `voice/`
- Contains standalone voice recognition tests (`voice.py`).
- Used to debug the voice command subsystem in isolation.

---

## Note
- None of these modules are required for the main rover execution.