# Hardware & Electronics Specification

This document details the hardware architecture of the **Genesis** rover.

## Power Subsystem
* **Primary Source:** 14.8V 4-cell Lithium Polymer (LiPo) Battery.
* **Secondary Source:** 5V Power Bank (for Jetson Nano).
* **Regulation:**
    * **Custom PCB:** Acts as a shield for the Arduino Mega and manages power distribution.
    * **Buck Converter:** LM2596 steps down 12V to 9V for the manipulator arm.

## Component List

| Component | Role | Specification |
| :--- | :--- | :--- |
| **Nvidia Jetson Nano** | Main Brain | 4GB Model, runs AI & Vision |
| **Arduino Mega 2560** | Motion Controller | Handles PWM for Drive Motors |
| **BTS7960** | Motor Drivers | High-current drivers for 6-wheel drive |
| **PCA9685** | PWM Driver | Generates precise signals for motor drivers |
| **Intel RealSense D415** | Depth Camera | Stereo vision for obstacle avoidance |

## Mechanical Design
* **Suspension:** Triple Bogie mechanism for load distribution and shock absorption.
* **Wheels:** 10cm diameter, 4.4cm width (Commercial Off-The-Shelf).

## Communication
* **Radio:** 3DR 433MHz Telemetry module for long-range manual control.
* **Wi-Fi:** For video streaming and short-range telemetry.