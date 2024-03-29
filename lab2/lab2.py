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


# HELPERS START
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


def colors(N):
    global COLORS

    COLORS = [[[50] * 3 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            COLORS[i][j][0] = random.randint(0, 255)
            COLORS[i][j][1] = random.randint(0, 255)
            COLORS[i][j][2] = random.randint(0, 255)
# HELPERS END


# 3.0
def points(N):
    u, v = compute_uv(N)
    points_array = compute_points(u, v)

    glBegin(GL_POINTS)
    for i in range(N):
        for j in range(N):
            glVertex3f(*points_array[i][j])
    glEnd()


# 3.5
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


# 4.0
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


# 4.5
def triangles_strip(N):
    u, v = compute_uv(N)
    points_array = compute_points(u, v)

    if not COLORS:
        colors(N)

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3ub(COLORS[i][j][0], COLORS[i][j][1], COLORS[i][j][2])
            glVertex3f(*points_array[i][j])
            glColor3ub(COLORS[i+1][j][0], COLORS[i+1][j][1], COLORS[i+1][j][2])
            glVertex3f(*points_array[i+1][j])
        glEnd()

# 5.0
def sierpinski_pyramid(N):
    sierpinski_helper(-5.0,-5.0,-5.0,10,10,N)


def sierpinski_helper(x,y,z,a,h,N):
    # base
    if not N:
        b = (x, y, z)
        c = (x + a, y, z)
        d = (x, y, z + a)
        e = (x + a, y, z + a)
        f = (x + a/2, y + h, z + a/2)

        pyramid(b,c,d,e,f)
        return



    # recursion
    sierpinski_helper(x, y, z, a / 2, h / 2, N - 1)
    sierpinski_helper(x + a / 2, y, z, a / 2, h / 2, N - 1)
    sierpinski_helper(x, y, z + a / 2, a / 2, h / 2, N - 1)
    sierpinski_helper(x + a / 2, y, z + a / 2, a / 2, h / 2, N - 1)
    sierpinski_helper(x + a / 4, y + h / 2, z + a / 4, a / 2, h / 2, N - 1)


def pyramid(a,b,c,d,e):
    # base
    glBegin(GL_TRIANGLE_STRIP)
    glColor3ub(255, 153, 51)
    glVertex3f(*a)
    glVertex3f(*b)
    glVertex3f(*c)
    glVertex3f(*d)
    glEnd()

    # walls
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 153, 51)
    glVertex3f(*a)
    glVertex3f(*b)
    glVertex3f(*e)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3ub(255, 153, 51)
    glVertex3f(*c)
    glVertex3f(*b)
    glVertex3f(*e)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3ub(255, 153, 51)
    glVertex3f(*c)
    glVertex3f(*d)
    glVertex3f(*e)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3ub(255, 153, 51)
    glVertex3f(*a)
    glVertex3f(*d)
    glVertex3f(*e)
    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time)
    axes()
    # points(100)
    # lines(25)
    # triangles(30)
    # triangles_strip(30)
    sierpinski_pyramid(3)
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
