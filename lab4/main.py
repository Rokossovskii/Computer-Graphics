#!/usr/bin/env python3
import sys

import numpy as np
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
from viever import Viever
from light import Light
from object import Object_in_3D

theta = 0.0
phi = 0.0
pix2angle = 1.0

left_mouse_button_pressed = 0
mouse_x_pos_old = 0
mouse_y_pos_old = 0
delta_x = 0
delta_y = 0

objects = []
light_sources = []
viewers = []
objects_types = [objects,light_sources,viewers]
objects_names = ["obiekty","zrodla_swiatla","obserwatorzy"]
parameter_name = ['ambient', 'diffuse', 'specular']
patameter_type = 0
parameter = 0
option = 0
entity_number = 0
choosen_type = 0

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
    global choosen_type
    global patameter_type
    global parameter
    global entity_number
    global option

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    
    if key == GLFW_KEY_N and action == GLFW_PRESS:
        choosen_type = (choosen_type + 1)%3
        entity_number %= len(objects_types[choosen_type])
        print(objects_names[choosen_type] + " " + str(entity_number))

    if key == GLFW_KEY_O and action == GLFW_PRESS:
        if choosen_type == 1:
            if(light_sources[entity_number].on_off()):
                print("on")
            else:
                print("off")
    
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        entity_number = (entity_number - 1)%len(objects_types[choosen_type])
        print(objects_names[choosen_type] + " " + str(entity_number))
    
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        entity_number = (entity_number + 1)%len(objects_types[choosen_type])
        print(objects_names[choosen_type] + " " + str(entity_number))

    if choosen_type == 1:
        if key == GLFW_KEY_UP and action == GLFW_PRESS:
            parameter = (parameter + 1)%4
            print(parameter_name[patameter_type] + " " + str(parameter))

        if key == GLFW_KEY_DOWN and action == GLFW_PRESS:
            parameter = (parameter + 1)%4
            print(parameter_name[patameter_type] + " " + str(parameter))

        if key == GLFW_KEY_LEFT and action == GLFW_PRESS:
            light_sources[entity_number].sub_light_settings(patameter_type,parameter)
            
        if key == GLFW_KEY_RIGHT and action == GLFW_PRESS:
            light_sources[entity_number].add_light_settings(patameter_type,parameter)
        
        if key == GLFW_KEY_KP_SUBTRACT and action == GLFW_PRESS:
            patameter_type = (patameter_type + 1 )%3
            print(parameter_name[patameter_type])

        if key == GLFW_KEY_KP_ADD and action == GLFW_PRESS:
            
            patameter_type = (patameter_type - 1 )%3
            print(parameter_name[patameter_type])
            

def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old
    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0



def render(time):
    global theta
    global phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    for viewer in viewers:
        gluLookAt(*viewer.get_position(),
                0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle/10
        phi +=delta_y * pix2angle/10
    
    if choosen_type == 1:
        light_sources[entity_number].move_light(theta,phi)

    glRotatef(theta, 0.0, 1.0, 0.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 3.0, 10, 10)
    gluDeleteQuadric(quadric)

    glFlush()



def startup():
    global objects
    global light_sources
    global viewers
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    obj0 = np.array([[1.0, 1.0, 1.0, 1.0],
                     [1.0, 1.0, 1.0, 1.0],
                     [1.0, 1.0, 1.0, 1.0]])
    obj0_shiness = 20.0

    light0 = np.array([[0.3, 0.0, 0.0, 0.0],
                       [0.8, 0.8, 0.0, 1.0],
                       [1.0, 1.0, 1.0, 1.0],
                       [0.0, -10.0, 0.0, 1.0]])

    light1 = np.array([[0.0, 0.0, 0.3, 0.0],
                       [0.8, 0.8, 0.0, 1.0],
                       [1.0, 1.0, 1.0, 1.0],
                       [0.0, 10.0, 0.0, 1.0]])

    objects.append(Object_in_3D(obj0,obj0_shiness))
    light_sources.append(Light(GL_LIGHT0,light0))
    light_sources.append(Light(GL_LIGHT1,light1))

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)

def shutdown():
    pass

def run(window):
    
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()

def main():

    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    viewers.append(Viever([0.0,0.0,10.0]))

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    run(window)
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()