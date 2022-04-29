# coding=utf-8
import glfw
from OpenGL.GL import *
import numpy as np
import sys, os.path

#Local 'grafica' imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from grafica.gpu_shape import GPUShape
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
from grafica.assets_path import getAssetPath

__author__ = "Vicente Guzmán Pinto"
__license__ = "MIT"


### Controller and Buttons Area ###
# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.useGravity = True

# global controller as communication with the callback function
controller = Controller()

# List of all keyboard calls
def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    elif key == glfw.KEY_UP:
        pass


### Execution Area ###
if __name__ == "__main__":

    ### Config Area ###
    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    # Size of app window
    width = 720
    height = 720

    window = glfw.create_window(width, height, "Flappy Bird", None, None)
    
    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # A simple shader program with position and texture coordinates as inputs.
    pipeline = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.25, 0.25, 0.25, 1.0)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    ### Shapes Area ###

    # Creating shapes on GPU memory
    # Flappy Bird Shape
    shapeBird = bs.createTextureQuad(1, 1.5)
    gpuBird = GPUShape().initBuffers()
    pipeline.setupVAO(gpuBird)
    gpuBird.fillBuffers(shapeBird.vertices, shapeBird.indices, GL_STATIC_DRAW)
    gpuBird.texture = es.textureSimpleSetup(
        getAssetPath("sprites\\yellowbird-upflap.png"), GL_CLAMP_TO_BORDER, GL_CLAMP_TO_BORDER, GL_NEAREST, GL_NEAREST)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        ## Drawing the shapes
        #Bird shape
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.scale(1.0, 1.0, 1.0)]))
        pipeline.drawCall(gpuBird)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuBird.clear()

    glfw.terminate()