import glfw
from OpenGL.GL import *
import numpy as np
from lib.utils import keyHandler, createWindow, sendVertices
from lib.Cube import Cube
from lib import globals

# Shader filenames
VERTEX_SHADER_FNAME = './lib/vertex_shader.glsl'
FRAGMENT_SHADER_FNAME = './lib/fragment_shader.glsl'

def main():
    # Define the global lock variable
    globals.lock_rotation = False

    # Load shader files
    vertex_code = open(VERTEX_SHADER_FNAME, 'r').read()
    fragment_code = open(FRAGMENT_SHADER_FNAME, 'r').read()

    # Create window, program and set key handler used to control the cube
    window, globals.program = createWindow(vertex_code, fragment_code)
    glfw.set_key_callback(window, keyHandler)
    
    # Define the global cube instance
    globals.cube = Cube()    

    # Get the vertices from the cube and send them to the GPU
    vertices = globals.cube.getVertices()
    sendVertices(globals.program, vertices)

    # Set the window to be visible and the background color
    glfw.show_window(window)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)

    # First simple camera rotation to show the cube in a 3D perspective
    globals.cube.rotateCameraX(0.4).rotateCameraY(0.4).rotateCameraZ(0.4)

    # Main loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        # Draw the cube state in the window
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        globals.cube.draw(globals.program)
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()
