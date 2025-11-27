# Genesis Rover: Software & Algorithms Manual

This document details the software stack, algorithms, and logic flows powering the **Genesis** rover. It covers system architecture, autonomous navigation, AI interaction, and control logic.

## Table of Contents
1. [System Architecture](#1-system-architecture)
2. [Autonomous Navigation Algorithms](#2-autonomous-navigation-algorithms)
3. [AI & Interaction Stack](#3-ai--interaction-stack)
4. [Control Logic & Data Flow](#4-control-logic--data-flow)
5. [Streaming](#5-streaming)

---

## 1. System Architecture
The software is distributed across three processing units:

* **Nvidia Jetson Nano:** Handles high-level decision making, Computer Vision (RealSense), AI (Voice/Object Detection), and Host Communication.
* **Arduino Mega 2560:** Handles low-level motor control (PWM generation) and sensor interfacing (IMU, GPS, Magnetometer).

---

## 2. Autonomous Navigation Algorithms

### 2.1 GPS Guided Navigation
The rover navigates to specific waypoints using a continuous feedback loop.

**1. Position Determination:**
Latitude ($\varphi$) and Longitude ($\lambda$) are retrieved from the **Ublox Neo M8N** module.

**2. Bearing Calculation:**
The required heading ($\theta$) is calculated using the formula:

$$\theta = \text{atan2}(\sin(\Delta\lambda) \cdot \cos(\varphi_2), \cos(\varphi_1) \cdot \sin(\varphi_2) - \sin(\varphi_1) \cdot \cos(\varphi_2) \cdot \cos(\Delta\lambda))$$

**3. Distance Calculation (Haversine Formula):**
The distance ($d$) to the target is computed to check if the rover has arrived within the acceptance radius:

$$a = \sin^2(\Delta\varphi/2) + \cos(\varphi_1) \cdot \cos(\varphi_2) \cdot \sin^2(\Delta\lambda/2)$$
$$c = 2 \cdot \text{atan2}(\sqrt{a}, \sqrt{1-a})$$
$$d = R \cdot c$$

*(Where $R \approx 6,371$ km)*

**4. Compass Alignment:**
The rover compares the calculated Bearing against the **HMC5883L Magnetometer** heading and rotates the chassis until they align.

### 2.2 Obstacle Avoidance (Vision Pipeline)
Uses an **Intel RealSense D415** Depth Camera. The processing pipeline is as follows:

1.  **Preprocessing:**
    * **Decimation Filter:** Downsamples image to reduce noise.
    * **Spatial Filter:** Smooths data and fills small holes.
    * **Thresholding:** Pixels > 1.0 meter are filtered out to focus on immediate hazards.
2.  **Canny Edge Detection:**
    * **Gaussian Blur:** Reduces noise.
    * **Gradient Calculation:** Finds intensity changes.
    * **Non-Maximum Suppression:** Thins edges.
    * **Double Thresholding:** Classifies strong/weak edges.
    * **Hysteresis:** Connects weak edges to strong edges.
3.  **Avoidance Logic:**
    The system calculates the "Center of Mass" of detected obstacles to decide the steering direction:
    * **Left Obstacle:** Rover turns **Right**.
    * **Right Obstacle:** Rover turns **Left**.
    * **Clear Path:** Rover moves **Forward**.

---

## 3. AI & Interaction Stack

### 3.1 Object Detection
* **Model:** SSD-MobileNet-v2.
* **Dataset:** MS COCO (91 Classes including Person, Vehicle, Animal, Household items).
* **Optimization:** Uses **TensorRT** for real-time inference on the Jetson Nano.

### 3.2 Voice Interaction
The voice system enables hands-free control and Q&A.

* **ASR (Automatic Speech Recognition):**
    * **QuartzNet-15x5:** For full sentence transcription.
    * **MatchboxNet:** For command classification (Keywords: "Stop", "Go", "Left", "Right").

* **TTS (Text-to-Speech):**
    * **FastPitch:** Generates MEL spectrograms.
    * **HiFiGAN:** Vocoder that converts spectrograms to audio.

---

## 4. Control Logic & Data Flow

### 4.1 Manual Mode
1.  **GUI Input:** User presses `W`, `A`, `S`, `D` on the Base Station.
2.  **Telemetry:** Signal sent via **3DR 433MHz Radio**.
3.  **Decoding:** Jetson Nano interprets signal.
4.  **Execution:** Arduino Mega receives command $\rightarrow$ PCA9685 PWM Driver $\rightarrow$ BTS7960 Motor Driver.
---

## 5. Streaming (Planned)
Video is streamed from the onboard webcam/RealSense to the Base Station using **RTP (Real-time Transport Protocol)** over Wi-Fi for low-latency feedback.