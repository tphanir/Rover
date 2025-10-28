#!/usr/bin/env python3

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
import serial
import sys

# Adjust as needed for your platform
PORT = '/dev/ttyUSB0'  # e.g. 'COM3' on Windows
BAUD = 38400

# Global variables for orientation
roll = pitch = yaw = 0.0
# Global variables for acceleration
accX = accY = accZ = 0.0
# Toggle whether we apply yaw in the orientation
yaw_mode = True

def init_serial():
    """Try to open the serial port."""
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        return ser
    except serial.SerialException:
        print("Failed to open serial port. Check the port name and try again.")
        sys.exit(1)

def resize(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(width)/float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init_gl():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def draw_text(position, text_string):
    font = pygame.font.SysFont("Courier", 18, True)
    text_surface = font.render(text_string, True, (255,255,255,255), (0,0,0,255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def draw_box():
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

def draw_acceleration_vector(ax, ay, az):
    """
    Draw a line (arrow) from (0,0,0) to (ax, ay, az) in red.
    Because the box is big, we might want to scale it so 1.0g ~ 1.0 in length.
    """
    glLineWidth(3.0)
    glColor3f(1.0, 0.0, 0.0)  # red arrow

    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(ax, ay, az)  # end of arrow
    glEnd()

    # Optionally, draw a small cone or arrowhead at the end.
    # For simplicity, we'll just do lines:
    # direction vector (ax, ay, az)
    # We'll skip the fancy arrowhead for brevity.

def read_data(ser):
    global roll, pitch, yaw, accX, accY, accZ

    ser.write(b".")  # request data
    line = ser.readline().strip()
    # Expect: "roll, pitch, yaw, accX, accY, accZ"
    parts = line.split(b", ")
    if len(parts) == 6:
        try:
            roll  = float(parts[0])
            pitch = float(parts[1])
            yaw   = float(parts[2])
            accX  = float(parts[3])
            accY  = float(parts[4])
            accZ  = float(parts[5])
        except ValueError:
            pass

def main():
    global yaw_mode

    ser = init_serial()

    pygame.init()
    screen = pygame.display.set_mode((640, 480), OPENGL|DOUBLEBUF)
    pygame.display.set_caption("Press Esc to quit, Z to toggle Yaw, A to toggle arrow scale")
    resize(640, 480)
    init_gl()

    frames = 0
    ticks = pygame.time.get_ticks()

    # Just in case you want to scale the acceleration vector
    # so it's more visible or smaller in the 3D space
    arrow_scale = 1.0

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_z:
                    yaw_mode = not yaw_mode
                elif event.key == K_a:
                    arrow_scale += 0.5
                    print(f"Acceleration Arrow scale = {arrow_scale}")

        # Read data from IMU
        read_data(ser)

        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Position camera
        glTranslatef(0, 0, -7.0)

        # 2D text overlay: show orientation & acceleration
        txt = (f"Roll: {roll:.2f} | Pitch: {pitch:.2f} | Yaw: {yaw:.2f} | "
               f"AccX: {accX:.2f}g | AccY: {accY:.2f}g | AccZ: {accZ:.2f}g")
        draw_text((-3, -3, 2), txt)

        # 1) Yaw rotation if yaw_mode is on
        if yaw_mode:
            glRotatef(yaw, 0.0, 1.0, 0.0)
        # 2) Pitch rotation
        glRotatef(pitch, 1.0, 0.0, 0.0)
        # 3) Roll rotation (negative sign is common for roll-axis orientation)
        glRotatef(-roll, 0.0, 0.0, 1.0)

        # Draw the box
        draw_box()

        # Now draw the acceleration vector in the same coordinate space
        # (0,0,0) to (accX, accY, accZ) scaled by arrow_scale
        draw_acceleration_vector(accX*arrow_scale, accY*arrow_scale, accZ*arrow_scale)

        pygame.display.flip()
        frames += 1

    # Print frames per second
    end_ticks = pygame.time.get_ticks()
    elapsed_ms = end_ticks - ticks
    if elapsed_ms > 0:
        fps = (frames * 1000) / elapsed_ms
        print(f"FPS: {fps:.2f}")

    ser.close()
    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()

