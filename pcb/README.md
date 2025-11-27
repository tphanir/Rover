# PCB Design & Hardware

This directory contains the manufacturing files for the custom **Power Distribution and Control Board** used in Rover Genesis 2. This board manages power delivery from the battery to the Jetson Nano, Arduino Mega, and motor drivers.

## File Overview

### `schematic.pdf`
The complete circuit diagram of the custom board. It details:
* **Power Regulation:** Buck converters for 5V (Jetson/Arduino) and 12V/VIN (Motors).
* **Pinout Connections:** Headers for connecting the Jetson Nano, Arduino, and sensors.
* **Protection:** Fuses and reverse polarity protection logic.

### `gerbers.zip`
The zipped Gerber files required for manufacturing the Printed Circuit Board (PCB). This file includes:
* **Copper Layers:** Top (GTL) and Bottom (GBL).
* **Solder Mask:** Top (GTS) and Bottom (GBS).
* **Silkscreen:** Component labels and logos (GTO).
* **Drill Files:** Hole locations and sizes (DRL).

## Fabrication Instructions

To manufacture this board, upload `gerbers.zip` to a PCB fabrication service (e.g., JLCPCB, PCBWay, OSH Park).

## Visuals
For 2D and 3D renders of this board, see the [docs/media/pcb](../docs/media/pcb) directory.