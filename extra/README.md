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

### `serial_test/`
- Contains serial communcation testing code. (`radio.py')
- It reads and relays command data from control computer (base station).


### `detection`
- Contains multiple programs (obstacle_x.py) that have been developed for obstacle detection applying various CV methods.
- Requires realsense camera to test.

## Note
- None of these modules are required for main rover execution.  
