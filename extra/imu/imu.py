#!/usr/bin/env python3
import sys, time, glob
import serial
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# ----- Serial config -----
BAUD = 38400
ser = None
connected = False

# Orientation variables
ax = ay = az = 0.0
yaw_mode = False
demo_angle = 0.0  # used when IMU not connected

def find_serial_port():
    """Scan for available serial ports."""
    ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
    return ports[0] if ports else None

def connect_serial():
    """Try connecting to the first available port."""
    global ser, connected
    port = find_serial_port()
    if not port:
        connected = False
        return
    try:
        ser = serial.Serial(port, BAUD, timeout=1)
        connected = True
        print(f"[INFO] Connected to {port}")
    except serial.SerialException:
        connected = False

def read_data():
    """Read IMU data if connected; else return demo rotation."""
    global ax, ay, az, demo_angle, connected

    if not connected:
        # simulate slow rotation if no IMU
        demo_angle += 0.5
        if demo_angle >= 360:
            demo_angle = 0
        ax = demo_angle / 2
        ay = demo_angle / 3
        az = demo_angle / 4
        # try reconnect occasionally
        if int(time.time()) % 3 == 0:
            connect_serial()
        return

    try:
        ser.write(b".")
        line = ser.readline().decode().strip()
        parts = line.split(",")
        if len(parts) == 3:
            ax, ay, az = map(float, parts)
    except (serial.SerialException, OSError):
        print("[WARN] Serial disconnected.")
        connected = False
        ser.close()
    except ValueError:
        pass

def resize(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init_gl():
    glShadeModel(GL_SMOOTH)
    glClearColor(0, 0, 0, 0)
    glClearDepth(1)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def draw_text(position, text):
    font = pygame.font.SysFont("Courier", 18, True)
    surface = font.render(text, True, (255, 255, 255))
    data = pygame.image.tostring(surface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(surface.get_width(), surface.get_height(),
                 GL_RGBA, GL_UNSIGNED_BYTE, data)

def draw_box():
    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)  # top
    glVertex3f( 1, 0.2, -1); glVertex3f(-1, 0.2, -1)
    glVertex3f(-1, 0.2,  1); glVertex3f( 1, 0.2,  1)
    glColor3f(1.0, 0.5, 0.0)  # bottom
    glVertex3f( 1, -0.2,  1); glVertex3f(-1, -0.2,  1)
    glVertex3f(-1, -0.2, -1); glVertex3f( 1, -0.2, -1)
    glColor3f(1, 0, 0)        # front
    glVertex3f( 1, 0.2, 1); glVertex3f(-1, 0.2, 1)
    glVertex3f(-1,-0.2, 1); glVertex3f( 1,-0.2, 1)
    glColor3f(1, 1, 0)        # back
    glVertex3f( 1,-0.2,-1); glVertex3f(-1,-0.2,-1)
    glVertex3f(-1, 0.2,-1); glVertex3f( 1, 0.2,-1)
    glColor3f(0, 0, 1)        # left
    glVertex3f(-1, 0.2, 1); glVertex3f(-1, 0.2,-1)
    glVertex3f(-1,-0.2,-1); glVertex3f(-1,-0.2, 1)
    glColor3f(1, 0, 1)        # right
    glVertex3f( 1, 0.2,-1); glVertex3f( 1, 0.2, 1)
    glVertex3f( 1,-0.2, 1); glVertex3f( 1,-0.2,-1)
    glEnd()

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -7.0)
    draw_text((-2, -2, 2), f"Pitch: {ay:.2f} Roll: {ax:.2f} Yaw: {az:.2f}")

    # apply rotations
    if yaw_mode:
        glRotatef(az, 0, 1, 0)
    glRotatef(ay, 1, 0, 0)
    glRotatef(-ax, 0, 0, 1)
    draw_box()

def main():
    global yaw_mode
    connect_serial()

    pygame.init()
    screen = pygame.display.set_mode((640, 480), OPENGL | DOUBLEBUF)
    pygame.display.set_caption("IMU Visualizer — Esc to quit, Z to toggle yaw")
    resize(640, 480)
    init_gl()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                if ser:
                    ser.close()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_z:
                yaw_mode = not yaw_mode
                if connected:
                    ser.write(b"z")

        read_data()
        draw_scene()
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
