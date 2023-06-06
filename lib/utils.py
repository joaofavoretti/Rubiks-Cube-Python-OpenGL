import glfw
import numpy as np
from OpenGL.GL import *
from lib import globals

def applyShaders(vert_code, frag_code):
    """
        Execute the correct pipeline to apply the shaders to the program

        vert_code(str) - Vertex shader code
        frag_code(str) - Fragment shader code
    """

    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    glShaderSource(vertex, vert_code)
    glShaderSource(fragment, frag_code)

    glCompileShader(vertex)
    glCompileShader(fragment)

    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    glLinkProgram(program)
    glUseProgram(program)

    return program

def createWindow(vert_code, frag_code):
    """
        Execute the correct pipeline to create the window and apply the shaders

        vert_code(str) - Vertex shader code
        frag_code(str) - Fragment shader code
    """

    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(700, 700, "Cubo", None, None)
    glfw.make_context_current(window)

    program = applyShaders(vert_code, frag_code)

    return window, program

def sendVertices(program, vertices):
    """
        Send the vertices to the GPU

        program(OpenGL.GL.shaders.ShaderProgram) - Shader program
        vertices(numpy.ndarray) - Vertices to be sent to the GPU
    """

    buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)

    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)

    glVertexAttribPointer(loc, 3, GL_FLOAT, False, stride, offset)

def keyHandler(window, key, scancode, action, mods):
    """
        Handle the key events

        window(glfw._GLFWwindow) - Window
        key(int) - Key code
        scancode(int) - Scancode
        action(int) - Action code
        mods(int) - Modifiers
    """
    
    # Camera Scale
    if key == glfw.KEY_I:
        globals.cube.scale(1.1)
    if key == glfw.KEY_O:
        globals.cube.scale(1.0/1.1)
    # Camera Rotation
    if key == glfw.KEY_UP:
        globals.cube.rotateCameraX(0.1)

    if key == glfw.KEY_DOWN:
        globals.cube.rotateCameraX(-0.1)

    if key == glfw.KEY_LEFT:
        globals.cube.rotateCameraY(0.1)

    if key == glfw.KEY_RIGHT:
        globals.cube.rotateCameraY(-0.1)

    # Camera Translation
    if key == glfw.KEY_Z:
        globals.cube.translateCameraZ(0.1)

    if key == glfw.KEY_X:
        globals.cube.translateCameraZ(-0.1)

    if key == glfw.KEY_C:
        globals.cube.translateCameraY(0.1)

    if key == glfw.KEY_V:
        globals.cube.translateCameraY(-0.1)

    if key == glfw.KEY_B:
        globals.cube.translateCameraX(0.1)

    if key == glfw.KEY_N:
        globals.cube.translateCameraX(-0.1)

    # Debug:
    if key == glfw.KEY_P:
        print(globals.cube.is_solved())

    # Face Rotations
    if globals.lock_rotation == True:
        return
    
    if key == glfw.KEY_Q and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (1, 0, 0), np.pi/2)
    
    if key == glfw.KEY_A and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (1, 0, 0), -np.pi/2)

    if key == glfw.KEY_W and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (-1, 0, 0), np.pi/2)

    if key == glfw.KEY_S and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (-1, 0, 0), -np.pi/2)

    if key == glfw.KEY_E and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (0, 1, 0), np.pi/2)

    if key == glfw.KEY_D and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (0, 1, 0), -np.pi/2)

    if key == glfw.KEY_R and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (0, -1, 0), np.pi/2)

    if key == glfw.KEY_F and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (0, -1, 0), -np.pi/2)

    if key == glfw.KEY_T and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (0, 0, 1), np.pi/2)

    if key == glfw.KEY_G and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (0, 0, 1), -np.pi/2)

    if key == glfw.KEY_Y and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (0, 0, -1), np.pi/2)

    if key == glfw.KEY_H and action == glfw.PRESS:
        globals.cube.drawSlowRotateFace(window, globals.program, (0, 0, -1), -np.pi/2)

    