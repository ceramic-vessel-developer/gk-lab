#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math, numpy


viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0
R = 10

vectors_visible = 0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
delta_y = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

# LIGHT0
light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

# LIGHT1
light_ambient1 = [0.0, 0.1, 0.1, 1.0]
light_diffuse1 = [0.0, 0.8, 0.8, 1.0]
light_specular1 = [1.0, 1.0, 1.0, 1.0]
light_position1 = [5.0, 5.0, 10.0, 1.0]

att_constant1 = 1.0
att_linear1 = 0.1
att_quadratic1 = 0.005

choice = [0, 0]

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    lights()


def lights():

    # LIGHT0
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    # LIGHT1
    glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular1)
    glLightfv(GL_LIGHT1, GL_POSITION, light_position1)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant1)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear1)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic1)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)


def shutdown():
    pass


def render(time):
    global theta, phi, light_position

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    # glRotatef(theta, 0.0, 1.0, 0.0)

    theta %= 360
    phi %= 360

    light_position[0] = R * math.cos(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    light_position[1] = R * math.sin(phi * math.pi / 180)
    light_position[2] = R * math.sin(theta * math.pi / 180) * math.cos(phi * math.pi / 180)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # quadric = gluNewQuadric()
    # gluQuadricDrawStyle(quadric, GLU_FILL)
    # gluSphere(quadric, 3.0, 10, 10)
    # gluDeleteQuadric(quadric)
    egg(20)
    # light visualization
    glTranslatef(light_position[0], light_position[1], light_position[2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glTranslatef(-light_position[0], -light_position[1], -light_position[2])



    glFlush()


def egg(N):
    u, v = compute_uv(N)
    points_array, vector_array = compute_points(u, v)

    for i in range(N - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glNormal3fv(vector_array[i][j])
            glVertex3f(*points_array[i][j])
            glNormal3fv(vector_array[i+1][j])
            glVertex3f(*points_array[i+1][j])
        glEnd()
    if vectors_visible:
        glBegin(GL_LINES)
        for i in range(N):
            for j in range(N):
                glVertex3fv(points_array[i][j])
                glVertex3fv(numpy.add(vector_array[i][j],  points_array[i][j]))
        glEnd()


def compute_points(u, v):
    N = len(u)
    points_array = [[[0] * 3 for _ in range(N) ]for _ in range(N)]
    vector_array = []

    for i in range(N):
        vector_array.append([])
        for j in range(N):
            points_array[i][j] = compute_xyz(u[i], v[j])
            vector = compute_vector(u[i], v[j])
            if i > N / 2:
                vector = [-1 * v for v in vector]
            vector_array[i].append(vector)

    vector_array[0][0] = [0, -1, 0]
    vector_array[N-1][N-1] = [0, 1, 0]

    return points_array, vector_array


def compute_uv(N):
    u = [(1/(N-1)) * i for i in range(N-1)]
    u.append(1.0)
    v = [(1/(N-1)) * i for i in range(N-1)]
    v.append(1.0)

    return u, v


def compute_xyz(u, v):
    x = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.cos(math.pi*v)
    y = 160 * u**4 - 320 * u**3 + 160 * u**2 - 5
    z = (-90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u) * math.sin(math.pi*v)

    return [x, y, z]


def compute_vector(u,v):
    x_u = (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 *
        u - 45) * math.cos(math.pi * v)
    x_v = math.pi * (
            90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 *
            u) * math.sin(math.pi * v)
    y_u = (640 * u ** 3 - 960 * u ** 2 + 320 * u)
    y_v = 0
    z_u = (-450 * u ** 4 + 900 * u ** 3 - 810 * u ** 2 + 360 *
        u - 45) * math.sin(math.pi * v)
    z_v = -math.pi * (
            90 * u ** 5 - 225 * u ** 4 + 270 * u ** 3 - 180 * u ** 2 + 45 *
            u) * math.cos(math.pi * v)

    vector = [y_u * z_v - z_u * y_v, z_u * x_v - x_u * z_v, x_u * y_v - y_u * x_v]

    length = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)
    if length == 0:
        length = 1
    vector = [vector[0] / length, vector[1] / length, vector[2] / length]

    return vector


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global choice, vectors_visible
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_C and action == GLFW_PRESS:
        choice[0] += 1
        choice[1] += 1 if choice[0] == 3 else 0
        choice[0] = choice[0] % 3
        choice[1] = choice[1] % 3
        print_choice()

    if key == GLFW_KEY_U and action == GLFW_PRESS:
        increase_colour(0.1)

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        decrease_colour(0.1)

    if key == GLFW_KEY_V and action == GLFW_PRESS:
        vectors_visible = not vectors_visible

def increase_colour(step):
    global light_ambient, light_diffuse, light_specular
    if choice[1] == 0:
        if step + light_ambient[choice[0]] <= 1.0:
            light_ambient[choice[0]] += step
        print(light_ambient)
    elif choice[1] == 1:
        if step + light_diffuse[choice[0]] <= 1.0:
            light_diffuse[choice[0]] += step
        print(light_diffuse)
    else:
        if step + light_specular[choice[0]] <= 1.0:
            light_specular[choice[0]] += step
        print(light_specular)
    lights()


def decrease_colour(step):
    global light_ambient, light_diffuse, light_specular
    if choice[1] == 0:
        if light_ambient[choice[0]] - step >= 0.0:
            light_ambient[choice[0]] -= step
        print(light_ambient)
    elif choice[1] == 1:
        if light_diffuse[choice[0]] - step >= 0.0:
            light_diffuse[choice[0]] -= step
        print(light_diffuse)
    else:
        if light_specular[choice[0]] - step >= 0.0:
            light_specular[choice[0]] -= step
        print(light_specular)
    lights()


def print_choice():
    if choice[1] == 0:
        print(f"Changing ambient, argument num{choice[0]}")
    elif choice[1] == 1:
        print(f"Changing diffuse, argument num{choice[0]}")
    else:
        print(f"Changing specular, argument num{choice[0]}")


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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