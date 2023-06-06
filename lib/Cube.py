import glfw
import numpy as np
from lib import globals
from OpenGL.GL import *
from lib.Cubie import Cubie

X_FACE_IDX = 0
Y_FACE_IDX = 1
Z_FACE_IDX = 2

class Cube:
    """
        Cube class that controls the cubies and the camera movements
    """

    def __init__(self):
        # Define the cubies list
        self.cubies = self.generateCubies()
    
    def is_solved(self):
        return all([cubie.is_solved() for cubie in self.cubies])

    def generateCubies(self):
        """
            Generate a 3x3x3 cube with the cubies in the correct positions
        """
        cubies = []
        len = 0.15

        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                for k in range(-1, 2, 1):
                    cubies.append(Cubie((i, j, k), len))

        return cubies
    
    def getVertices(self):
        """
            Combine the vertices of all the cubies in a single matrix using the cubies order in the self.cubies list
        """
        vertices = np.empty((0, 3), dtype=np.float32)
        for cubie in self.cubies:
            vertices = np.vstack((vertices, cubie.getVertices()))
        return vertices
    
    def scale(self, s):
        """
            Scale the cube by a factor s
            s(float) - Scale factor
        """
        for cubie in self.cubies:
            cubie.scale(s)

    def rotateX(self, ang):
        """
            Rotate the cube around the X axis by an angle ang. Rotates each cubie individually
            ang(float) - Rotation angle
        """
        for cubie in self.cubies:
            cubie.rotateX(ang)
        return self
    
    def rotateCameraX(self, ang):
        """
            Rotate the cube camera around the X axis by an angle ang. Rotates each cubie individually
            ang(float) - Rotation angle
        """
        for cubie in self.cubies:
            cubie.rotateCameraX(ang)
        return self

    def rotateY(self, ang):
        """
            Rotate the cube around the Y axis by an angle ang. Rotates each cubie individually
            ang(float) - Rotation angle
        """
        for cubie in self.cubies:
            cubie.rotateY(ang)
        return self
    
    def rotateCameraY(self, ang):
        """
            Rotate the cube camera around the Y axis by an angle ang. Rotates each cubie individually
            ang(float) - Rotation angle
        """
        for cubie in self.cubies:
            cubie.rotateCameraY(ang)
        return self
    
    def rotateZ(self, ang):
        """
            Rotate the cube around the Z axis by an angle ang. Rotates each cubie individually
            ang(float) - Rotation angle
        """
        for cubie in self.cubies:
            cubie.rotateZ(ang)
        return self
    
    def rotateCameraZ(self, ang):
        """
            Rotate the cube camera around the Z axis by an angle ang. Rotates each cubie individually
            ang(float) - Rotation angle
        """
        for cubie in self.cubies:
            cubie.rotateCameraZ(ang)
        return self
    
    def translateCameraX(self, dist):
        """
            Translate the cube camera along the X axis by a distance dist
            dist(float) - Translation distance
        """
        for cubie in self.cubies:
            cubie.translateCameraX(dist)
        return self
    
    def translateCameraY(self, dist):
        """
            Translate the cube camera along the Y axis by a distance dist
            dist(float) - Translation distance
        """
        for cubie in self.cubies:
            cubie.translateCameraY(dist)
        return self
    
    def translateCameraZ(self, dist):
        """
            Translate the cube camera along the Z axis by a distance dist
            dist(float) - Translation distance
        """
        for cubie in self.cubies:
            cubie.translateCameraZ(dist)
        return self
    
    
    def drawSlowRotateFace(self, window, program, face, ang):
        """
            Function to animate the rotation of a face of the cube
            The logic may be a little bit tricky

            window (glfw.window): Window to draw
            program (OpenGL.GL.shaders.ShaderProgram): Shader program to use
            face (tuple(int, int, int)): Face to rotate. Ex: (1, 0, 0) rotaciona a face que possui um cubie na posição (1, 0, 0)
            ang (float): Angle to rotate
        """
        
        # Lock the rotation of other faces during the animation of the current face
        globals.lock_rotation = True

        # Index of face that is equal to 1 or -1
        face_idx, face_value = [(i, x) for i, x in enumerate(face) if x == 1 or x == -1][0]

        # Define the number of steps used and the angle delta for each step 
        ang_steps = 20
        ang_dt = ang / ang_steps

        # Get the indexes of the cubies that are on the face to be rotated
        cubies_idx_on_face = [i for i, cubie in enumerate(self.cubies) if cubie.pos[face_idx] == face_value]

        # For each step in the animation
        for i in range(ang_steps):

            # Use different rotation functions depending on the face to be rotated

            if face_idx == X_FACE_IDX:
                for idx in cubies_idx_on_face:
                    self.cubies[idx].rotateX(ang_dt)

            elif face_idx == Y_FACE_IDX:
                for idx in cubies_idx_on_face:
                    self.cubies[idx].rotateY(ang_dt)

            elif face_idx == Z_FACE_IDX:
                for idx in cubies_idx_on_face:
                    self.cubies[idx].rotateZ(ang_dt)
            
            # Draw the cube
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw(program)
            glfw.swap_buffers(window)

        # Update the position variable on each cubie that was rotated
        if face_idx == 0:
            for idx in cubies_idx_on_face:
                self.cubies[idx].rotatePosX(ang)

        elif face_idx == 1:
            for idx in cubies_idx_on_face:
                self.cubies[idx].rotatePosY(ang)

        elif face_idx == 2:
            for idx in cubies_idx_on_face:
                self.cubies[idx].rotatePosZ(ang)

        # Unlock the rotation of other faces
        globals.lock_rotation = False

        return self

    def draw(self, program):
        """
            Draw the cube
        """
        for index, cubie in enumerate(self.cubies):
            cubie.draw(program, index * 24)
