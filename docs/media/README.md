# Project Media & Assets

This directory contains visual assets and debug images used to document the hardware design and software logic.

## Directory Overview

### cad/ (Mechanical Design)
Contains renders from the CAD software used to model the chassis.
* **rover-v2-isometric-cad-model.png**: An angled 3D view of the complete rover.
* **rover-v2-top-cad-model.png**: A top-down view showing component placement.

### main/ (System Overview)
General images related to the rover architecture.
* **architecture-diagram.png**: A block diagram connecting the Base Station, Jetson Nano, and Arduino.
* **rover.jpg**: A photograph of the assembled rover.

### obstacle_detection/ (Computer Vision Debug)
Visual outputs from the autonomous navigation module showing how the rover interprets depth data.
* **rgb-bbox.png**: Color camera feed with detected objects.
* **depth-bbox.png**: Depth map showing distance to objects.
* **threshold-map.png**: Binary image highlighting areas that are too close.
* **canny-edges.png**: Edge detection results used to define object boundaries.
* **obstacle-map.png**: The final processed map used for decision making.
* **decision-rotate-left.png**: Visualization of the logic deciding to turn left.

### pcb/ (Electronics)
Schematics and renders of the custom Power Distribution PCB.
* **2D-schematic-of-PCB-design.png**: The layout view of the PCB traces.
* **3D-schematic-of-PCB-design.png**: A 3D render of the manufactured board.