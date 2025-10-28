# extra/

This directory contains **miscellaneous experiments** developed during the evolution of the **Rover** project.  
While not part of the main rover control system, these files served as important learning points for specific features, hardware integration and testing purposes.

---

## Overview

### `imu/`
- Contains the IMU visualization and orientation tracking code (`imu.py`).
- Visualizes 3D motion of the rover (roll, pitch, yaw) using **PyOpenGL** and **pygame**.
- Works both with and without the physical ESP32-IMU connected:
  - If connected → reads live orientation data.
  - If not connected → runs in simulation mode showing a static/no-movement cube.

## Note
- None of these modules are required for main rover execution.  
- They can be run indi
