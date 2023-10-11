#!/usr/bin/env python3
import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


RED = random.randint(0,255)
GREEN = random.randint(0,255)
BLUE = random.randint(0,255)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

# 3.0
def triangle():
    # green part
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(25.0, 50.0)
    glVertex2f(50.0, 0.0)
    glEnd()

    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(25.0, 50.0)
    glVertex2f(0.0, 25.0)
    glEnd()

    # red part
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(-25.0, 50.0)
    glVertex2f(-50.0, 0.0)
    glEnd()

    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(0.0, 0.0)
    glVertex2f(-25.0, 50.0)
    glVertex2f(0.0, 25.0)
    glEnd()

    # blue part
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(25.0, 50.0)
    glVertex2f(-25.0, 50.0)
    glVertex2f(0.0, 100.0)
    glEnd()

    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(25.0, 50.0)
    glVertex2f(-25.0, 50.0)
    glVertex2f(0.0, 25.0)
    glEnd()

# 4.0
def rectangle(x,y,a,b,d = 0.0,R=RED,G=GREEN,B=BLUE):

    glColor3ub(R, G, B)
    glBegin(GL_TRIANGLES)
    glVertex2f(x-d, y-d)
    glVertex2f(x + a, y)
    glVertex2f(x, y + b)
    glEnd()

    glColor3ub(R, G, B)
    glBegin(GL_TRIANGLES)
    glVertex2f(x + a + d, y + b + d)
    glVertex2f(x + a, y)
    glVertex2f(x, y + b)
    glEnd()

# 4.5
def sierpinski_rec(i = 5):
    rectangle(-100,-100,200,200,0,172,63,9)
    sierpinski_rec_helper(-100,-100,200,200,i)

def sierpinski_rec_helper(x,y,a,b,i):
    if i == 0:
        return
    temp_a = a/3.0
    temp_b = b/3.0

    rectangle(x+temp_a,y+temp_b,temp_a,temp_b,0,255,255,255)

    sierpinski_rec(x,y,temp_a,temp_b,i-1)
    sierpinski_rec(x+temp_a,y,temp_a,temp_b,i-1)
    sierpinski_rec(x+ 2*temp_a,y,temp_a,temp_b,i-1)
    sierpinski_rec(x,y+temp_b,temp_a,temp_b,i-1)
    sierpinski_rec(x,y+2*temp_b,temp_a,temp_b,i-1)
    sierpinski_rec(x+2*temp_a,y+temp_b,temp_a,temp_b,i-1)
    sierpinski_rec(x+2*temp_a,y+2*temp_b,temp_a,temp_b,i-1)
    sierpinski_rec(x+temp_a,y+2*temp_b,temp_a,temp_b,i-1)

# 5.0
def sierpinski_tri(A,B,C,i):
    glColor3ub(172,63,9)
    glBegin(GL_TRIANGLES)
    glVertex2f(*A)
    glVertex2f(*B)
    glVertex2f(*C)
    glEnd()
    sierpinski_tri_helper(A, B, C, i)

def sierpinski_tri_helper(A,B,C,i):
    if not i:
        return

    nAB = [(B[0]+A[0])/2.0,(B[1]+A[1])/2.0]
    nBC = [(C[0]+B[0])/2.0,(C[1]+B[1])/2.0]
    nCA = [(C[0]+A[0])/2.0,(C[1]+A[1])/2.0]

    glColor3ub(0,0,0)
    glBegin(GL_TRIANGLES)
    glVertex2f(*nAB)
    glVertex2f(*nBC)
    glVertex2f(*nCA)
    glEnd()

    sierpinski_tri_helper(A,nAB,nCA,i-1)
    sierpinski_tri_helper(nAB,B,nBC,i-1)
    sierpinski_tri_helper(nCA,nBC,C,i-1)




def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    sierpinski_tri([-100,-100],[100,-100], [0,73.20508075688772], 5)

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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

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