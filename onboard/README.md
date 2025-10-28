# Rover Main System

This directory contains the main control software for the Rover project.  
It integrates all modules needed for manual, semi-autonomous, and fully autonomous navigation, gps-based navigation.

---

## Overview

### controls/
Contains programs handling different control modes:
- **fullauto.py** — Full autonomous navigation using Camera. 
- **gps.py** — GPS control instruction program.
- **semiauto.py** — Semi-autonomous control combining user input with automation.

### handlers/
Handles inputs, communication, and command processing:
- **manual.py** — Manual (keyboard/joystick) control.  
- **mega.py** — Arduino Mega communication handler.  
- **serial.py** — Serial communication between base station and rover.  
- **voice.py** — Voice command handling.

### helpers/
- **forward.py** — Forwards messages from Arduion mega to base_station.

### modules/
- **Camera.py** — Camera handling and video stream processing.

### VoiceNav/
- **main.py** — Voice navigation control.  
- **data.txt** — Voice data or recognized commands.  
- **echo.sh** — Voice test script.

### scripts/
- **docker.sh** — Docker script for setting up Jetson-Voice modules.
- **echo.sh** — Simply echoes the VoiceNav/data.txt content.

### main.py
- Main entry point — connects all modules for complete rover operation.

---
