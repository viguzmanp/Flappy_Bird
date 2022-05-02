# coding=utf-8
__author__ = "Vicente Guzmán Pinto"
__license__ = "MIT"

## Imports
import glfw
from OpenGL.GL import *
import numpy as np
import sys, os.path
from model import *
from controller import Controller

if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    # Window Settings
    width = 600
    height = 600
    window = glfw.create_window(width, height, 'Flappy Bird', None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)

    # Defines the controller
    controller = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear background color
    glClearColor(0, 0.7, 0.7, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Make the objects
    bird = Bird(pipeline)
    tubes = TubeFactory()
    controller.set_model(bird)
    controller.set_tubes(tubes)

    # Sets the initial time value
    t0 = 0

    # Defines gravity
    gravity = np.array([0, -15, 0], dtype = np.float32)

    while not glfw.window_should_close(window):  # Dibujando --> 1. obtener el input

        # Calculamos el dt
        ti = glfw.get_time()
        dt = ti - t0
        t0 = ti

        # Using GLFW to check for input events
        glfw.poll_events()  # OBTIENE EL INPUT --> CONTROLADOR --> MODELOS

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        tubes.create_tube(pipeline)
        tubes.updatePosition(dt)
        bird.updatePosition(gravity, dt)

        # Reconocer la logica
        bird.collide(tubes)  # ---> RECORRER TODOS LOS TUBOS

        # DIBUJAR LOS MODELOS
        tubes.draw(pipeline)
        bird.draw(pipeline)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    glfw.terminate()