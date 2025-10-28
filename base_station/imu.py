#!/usr/bin/env python3

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial
import sys

# ----- Configure your serial port here -----
# Windows Example: ser = serial.Serial('COM3', 38400, timeout=1)
# Mac/Linux Example: ser = serial.Serial('/dev/tty.usbserial', 38400, timeout=1)
try:
    ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
except serial.SerialException:
    print("Failed to open serial port. Check the port name and try again.")
    sys.exit(1)

# Global variables for orientation angles
ax = ay = az = 0.0
yaw_mode = False  # Toggles whether we rotate around Y-axis (yaw) in OpenGL

def resize(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def drawText(position, textString):
    """Helper to render text in the OpenGL window."""
    font = pygame.font.SysFont("Courier", 18, True)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, textData)

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Position the box a bit away from the camera
    glTranslatef(0.0, 0.0, -7.0)

    # Always show Pitch, Roll, and Yaw on screen
    osd_text = (
        f"Pitch: {ay:.2f}, "
        f"Roll: {ax:.2f}, "
        f"Yaw: {az:.2f}"
    )
    drawText((-2, -2, 2), osd_text)

    # Apply 3D rotations
    # 1) If yaw_mode is True, rotate around Y-axis by az
    if yaw_mode:
        glRotatef(az, 0.0, 1.0, 0.0)  # Yaw
    # 2) Then pitch around X-axis by ay
    glRotatef(ay, 1.0, 0.0, 0.0)
    # 3) Finally roll around Z-axis by ax (note we use -ax for the typical "roll" orientation)
    glRotatef(-ax, 0.0, 0.0, 1.0)

    # Draw a simple rectangular "box" to visualize orientation
    glBegin(GL_QUADS)

    # Top face (green)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f( 1.0,  0.2, -1.0)
    glVertex3f(-1.0,  0.2, -1.0)
    glVertex3f(-1.0,  0.2,  1.0)
    glVertex3f( 1.0,  0.2,  1.0)

    # Bottom face (orange)
    glColor3f(1.0, 0.5, 0.0)
    glVertex3f( 1.0, -0.2,  1.0)
    glVertex3f(-1.0, -0.2,  1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f( 1.0, -0.2, -1.0)

    # Front face (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f( 1.0,  0.2,  1.0)
    glVertex3f(-1.0,  0.2,  1.0)
    glVertex3f(-1.0, -0.2,  1.0)
    glVertex3f( 1.0, -0.2,  1.0)

    # Back face (yellow)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f( 1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0,  0.2, -1.0)
    glVertex3f( 1.0,  0.2, -1.0)

    # Left face (blue)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0,  0.2,  1.0)
    glVertex3f(-1.0,  0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2,  1.0)

    # Right face (magenta)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f( 1.0,  0.2, -1.0)
    glVertex3f( 1.0,  0.2,  1.0)
    glVertex3f( 1.0, -0.2,  1.0)
    glVertex3f( 1.0, -0.2, -1.0)

    glEnd()

def read_data():
    """Request one line of data (roll, pitch, yaw) from the ESP32/Arduino."""
    global ax, ay, az

    # Send a dot to request data
    ser.write(b".")
    line = ser.readline()

    # The Arduino should send "roll, pitch, yaw" in one line
    angles = line.split(b", ")
    if len(angles) == 3:
        try:
            ax = float(angles[0])  # treat as ROLL
            ay = float(angles[1])  # treat as PITCH
            az = float(angles[2])  # treat as YAW
        except ValueError:
            pass  # If conversion fails, ignore this loop

def main():
    global yaw_mode

    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    
    # Create a 640x480 window
    screen = pygame.display.set_mode((640, 480), video_flags)
    pygame.display.set_caption("Press Esc to quit, Z to toggle Yaw Rotation")
    resize(640, 480)
    init()

    frames = 0
    ticks = pygame.time.get_ticks()

    while True:
        # Event handling
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()  # Properly quit pygame
            break
        if event.type == KEYDOWN and event.key == K_z:
            yaw_mode = not yaw_mode
            # Optionally inform the Arduino if needed
            ser.write(b"z")

        # Read data from the IMU
        read_data()

        # Render the updated orientation
        draw()
        pygame.display.flip()
        frames += 1

    # Print frames per second, for reference
    end_ticks = pygame.time.get_ticks()
    elapsed_ms = end_ticks - ticks
    if elapsed_ms > 0:
        fps = (frames * 1000) / elapsed_ms
        print(f"FPS: {fps:.2f}")

    ser.close()

if __name__ == "__main__":
    main()

