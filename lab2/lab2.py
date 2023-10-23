#!/usr/bin/env python3
import math
import random
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

COLORS = []

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def compute_xyz(u, v):
    x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi*v)
    y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
    z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi*v)

    return [x, y, z]


def compute_points(u, v):
    N = len(u)
    points_array = [[[0] * 3 for _ in range(N) ]for _ in range(N)]

    for i in range(N):
        for j in range(N):
            points_array[i][j] = compute_xyz(u[i], v[j])

    return points_array


def compute_uv(N):
    u = [(1/(N-1)) * i for i in range(N-1)]
    u.append(1.0)
    v = [(1/(N-1)) * i for i in range(N-1)]
    v.append(1.0)

    return u, v


def points(N):
    u, v = compute_uv(N)
    points_array = compute_points(u, v)

    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3f(*points_array[i][j])
    glEnd()


def lines(N):
    u, v = compute_uv(N)
    points_array = compute_points(u, v)

    for i in range(N-1):
        for j in range(N-1):
            glBegin(GL_LINES)
            glVertex3f(*points_array[i][j])
            glVertex3f(*points_array[i+1][j])
            glEnd()
            glBegin(GL_LINES)
            glVertex3f(*points_array[i][j])
            glVertex3f(*points_array[i][j+1])
            glEnd()


def triangles(N):
    u, v = compute_uv(N)
    points_array = compute_points(u, v)

    if not COLORS:
        colors(N)


    for i in range(N-1):
        for j in range(N-1):
            glBegin(GL_TRIANGLES)
            glColor3ub(COLORS[i][j][0], COLORS[i][j][1], COLORS[i][j][2])
            glVertex3f(*points_array[i][j])
            glColor3ub(COLORS[i+1][j][0], COLORS[i+1][j][1], COLORS[i+1][j][2])
            glVertex3f(*points_array[i+1][j])
            glColor3ub(COLORS[i][j+1][0], COLORS[i][j+1][1], COLORS[i][j+1][2])
            glVertex3f(*points_array[i][j+1])
            glEnd()
            glBegin(GL_TRIANGLES)
            glColor3ub(COLORS[i+1][j][0], COLORS[i+1][j][1], COLORS[i+1][j][2])
            glVertex3f(*points_array[i+1][j])
            glColor3ub(COLORS[i][j+1][0], COLORS[i][j+1][1], COLORS[i][j+1][2])
            glVertex3f(*points_array[i][j+1])
            glColor3ub(COLORS[i+1][j+1][0], COLORS[i+1][j+1][1], COLORS[i+1][j+1][2])
            glVertex3f(*points_array[i+1][j + 1])
            glEnd()


def colors(N):
    global COLORS

    COLORS = [[[50] * 3 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            COLORS[i][j][0] = random.randint(0, 255)
            COLORS[i][j][1] = random.randint(0, 255)
            COLORS[i][j][2] = random.randint(0, 255)



def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time)
    axes()
    # points(100)
    # lines(25)
    triangles(30)
    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()