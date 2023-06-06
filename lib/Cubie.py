import numpy as np
from OpenGL.GL import *

class Cubie:
    """
        Cubie class that controls the vertices and the transformations of a single cubie
    """

    def __init__(self, position, len):
        """
            position(tuple(int, int, int)) - Position of the cubie in the cube
            len(float) - Length of the cubie
        """
        x, y, z = position
        
        # Seen coordinate from the cubie
        self.pos = (float(x), float(y), float(z), 1.0)
        self.len = len
        
        # Actual coordinate in the cube (opengl coordinate)
        self.central_verts = (x * 2 * len, y * 2 * len, z * 2 * len)
        self.verts = self.defineVertices(self.central_verts, self.len)
        
        # Transformation matrices used by camera and face movements
        self.mat = np.identity(4, dtype=np.float32)
        self.camera = np.identity(4, dtype=np.float32)
        self.camera_rotation = np.identity(4, dtype=np.float32)
        
        # Face colors for each cubie (Note: The face is colored, even though the face is not shown)
        self.colors = np.array([(1.0, 0.0, 0.0, 1.0),
                                (0.0, 0.0, 1.0, 1.0),
                                (1.0, 0.6, 0.0, 1.0),
                                (0.0, 1.0, 0.0, 1.0),
                                (1.0, 1.0, 1.0, 1.0),
                                (1.0, 1.0, 0.0, 1.0)])

    def is_solved(self):
        test_vertices = np.array([(self.mat @ np.array([vert[0], vert[1], vert[2], 1.0]).T) - np.array([vert[0], vert[1], vert[2], 1.0]).T for vert in self.verts])
        print(abs(test_vertices))
        return np.all(abs(test_vertices) < 1e-4)
        
    def defineVertices(self, pos, len):
        """
            Define the vertices of the cubie

            pos(tuple(float, float, float)) - Position of the cubie in the cube (opengl coordinate)
            len(float) - Length of the cubie
        """
        return np.array([

            (pos[0] - len, pos[1] - len, pos[2] + len),
            (pos[0] + len, pos[1] - len, pos[2] + len),
            (pos[0] - len, pos[1] + len, pos[2] + len),
            (pos[0] + len, pos[1] + len, pos[2] + len),

            (pos[0] + len, pos[1] - len, pos[2] + len),
            (pos[0] + len, pos[1] - len, pos[2] - len),
            (pos[0] + len, pos[1] + len, pos[2] + len),
            (pos[0] + len, pos[1] + len, pos[2] - len),

            (pos[0] + len, pos[1] - len, pos[2] - len),
            (pos[0] - len, pos[1] - len, pos[2] - len),
            (pos[0] + len, pos[1] + len, pos[2] - len),
            (pos[0] - len, pos[1] + len, pos[2] - len),

            (pos[0] - len, pos[1] - len, pos[2] - len),
            (pos[0] - len, pos[1] - len, pos[2] + len),
            (pos[0] - len, pos[1] + len, pos[2] - len),
            (pos[0] - len, pos[1] + len, pos[2] + len),

            (pos[0] - len, pos[1] - len, pos[2] - len),
            (pos[0] + len, pos[1] - len, pos[2] - len),
            (pos[0] - len, pos[1] - len, pos[2] + len),
            (pos[0] + len, pos[1] - len, pos[2] + len),

            (pos[0] - len, pos[1] + len, pos[2] + len),
            (pos[0] + len, pos[1] + len, pos[2] + len),
            (pos[0] - len, pos[1] + len, pos[2] - len),
            (pos[0] + len, pos[1] + len, pos[2] - len)
        ], dtype=np.float32)
    
    def getVertices(self):
        return self.verts
        
    def scale(self, s):
        """
            Scale the cubie

            s(float) - Scale factor
        """

        mat_scale = np.array([
            [s, 0, 0, 0],
            [0, s, 0, 0],
            [0, 0, s, 0],
            [0, 0, 0, 1]], dtype=np.float32)

        # Apply the scale to the camera
        self.camera = mat_scale @ self.camera

    # Use for visual rotation
    def rotateX(self, ang):
        """
            Rotate the cubie around the x-axis

            ang(float) - Angle of rotation
        """
        mat_rot_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(ang), -np.sin(ang), 0],
            [0, np.sin(ang), np.cos(ang), 0],
            [0, 0, 0, 1]
        ])

        # Apply the rotation to the cubie
        self.mat = mat_rot_x @ self.mat

        return self

    # Use for 90 deg rotation
    def rotatePosX(self, ang):
        """
            Rotate the cubie position around the x-axis

            ang(float) - Angle of rotation
        """
        mat_rot_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(ang), -np.sin(ang), 0],
            [0, np.sin(ang), np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        # Apply the rotation to the position of the cubie in the cube
        self.pos = mat_rot_x @ self.pos
        self.pos = np.round(self.pos)

        return self

    def rotateCameraX(self, ang):
        """
            Rotate the camera around the x-axis

            ang(float) - Angle of rotation
        """
        mat_rot_x = np.array([
            [1, 0, 0, 0],
            [0, np.cos(ang), -np.sin(ang), 0],
            [0, np.sin(ang), np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        # Apply the rotation to the camera
        self.camera_rotation = mat_rot_x @ self.camera_rotation
        
        return self

    # Use for visual rotation
    def rotateY(self, ang):
        """
            Rotate the cubie around the y-axis

            ang(float) - Angle of rotation
        """
        mat_rot_y = np.array([
            [np.cos(ang), 0, np.sin(ang), 0],
            [0, 1, 0, 0],
            [-np.sin(ang), 0, np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        # Apply the rotation to the cubie
        self.mat = mat_rot_y @ self.mat

        return self
    
    # Use for 90 deg rotation
    def rotatePosY(self, ang):
        """
            Rotate the cubie position around the y-axis

            ang(float) - Angle of rotation
        """
        mat_rot_y = np.array([
            [np.cos(ang), 0, np.sin(ang), 0],
            [0, 1, 0, 0],
            [-np.sin(ang), 0, np.cos(ang), 0],
            [0, 0, 0, 1]
        ])
        
        # Apply the rotation to the position of the cubie in the cube
        self.pos = mat_rot_y @ self.pos
        self.pos = np.round(self.pos)
        
        return self
    
    def rotateCameraY(self, ang):
        """
            Rotate the camera around the y-axis

            ang(float) - Angle of rotation
        """
        mat_rot_y = np.array([
            [np.cos(ang), 0, np.sin(ang), 0],
            [0, 1, 0, 0],
            [-np.sin(ang), 0, np.cos(ang), 0],
            [0, 0, 0, 1]
        ])

        # Apply the rotation to the camera
        self.camera_rotation = mat_rot_y @ self.camera_rotation
        
        return self

    # Use for visual rotation
    def rotateZ(self, ang):
        """
            Rotate the cubie around the z-axis

            ang(float) - Angle of rotation
        """
        mat_rot_z = np.array([
            [np.cos(ang), -np.sin(ang), 0, 0],
            [np.sin(ang), np.cos(ang), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # Apply the rotation to the cubie
        self.mat = mat_rot_z @ self.mat
        
        return self
    
    # Use for 90 deg rotation
    def rotatePosZ(self, ang):
        """
            Rotate the cubie position around the z-axis

            ang(float) - Angle of rotation
        """
        mat_rot_z = np.array([
            [np.cos(ang), -np.sin(ang), 0, 0],
            [np.sin(ang), np.cos(ang), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # Apply the rotation to the position of the cubie in the cube
        self.pos = mat_rot_z @ self.pos
        self.pos = np.round(self.pos)
        
        return self
    
    def rotateCameraZ(self, ang):
        """
            Rotate the camera around the z-axis

            ang(float) - Angle of rotation
        """
        mat_rot_z = np.array([
            [np.cos(ang), -np.sin(ang), 0, 0],
            [np.sin(ang), np.cos(ang), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        # Apply the rotation to the camera
        self.camera_rotation = mat_rot_z @ self.camera_rotation
        
        return self
    
    def translateCameraX(self, dist):
        """
            Translate the camera along the x-axis

            dist(float) - Distance to translate
        """
        mat_transl_x = np.array([
            [1, 0, 0, dist],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        # Apply the translation to the camera
        self.camera = mat_transl_x @ self.camera

        return self
    
    def translateCameraY(self, dist):
        """
            Translate the camera along the y-axis

            dist(float) - Distance to translate
        """
        mat_transl_y = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, dist],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        # Apply the translation to the camera
        self.camera = mat_transl_y @ self.camera

        return self
    
    def translateCameraZ(self, dist):
        """
            Translate the camera along the z-axis

            dist(float) - Distance to translate
        """
        mat_transl_z = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, dist],
            [0, 0, 0, 1]
        ])

        # Apply the translation to the camera
        self.camera = mat_transl_z @ self.camera

        return self

    def drawFace(self, program, vert_start_idx, face):
        """
            Draw a face of the cubie

            program(OpenGL.GL.shaders.ShaderProgram) - Shader program
            vert_start_idx(int) - Index of the first vertex of the cubie. Offset in the vertex array
            face(int) - Face to draw. Index in the vertex array of the cubie
        """
        
        loc_color = glGetUniformLocation(program, "color")
        
        # Draw the face of the cubie according the the color
        colorR, colorG, colorB, colorA = self.colors[face]
        glUniform4f(loc_color, colorR, colorG, colorB, colorA)
        glDrawArrays(GL_TRIANGLE_STRIP, vert_start_idx + face * 4, 4)

        # Draw the black border of the face        
        border_vertex_idx = np.array([vert_start_idx + face * 4 + 0, 
                                      vert_start_idx + face * 4 + 1,
                                      vert_start_idx + face * 4 + 3,
                                      vert_start_idx + face * 4 + 2,
                                      vert_start_idx + face * 4 + 0])
        
        glUniform4f(loc_color, 0.0, 0.0, 0.0, 1.0)
        glDrawElements(GL_LINE_STRIP, len(border_vertex_idx), GL_UNSIGNED_INT, border_vertex_idx)

    def draw(self, program, vert_start_idx):
        """
            Draw the cubie. Draw each face of the cubie separately

            program(OpenGL.GL.shaders.ShaderProgram) - Shader program
            vert_start_idx(int) - Index of the first vertex of the cubie. Offset in the vertex array
        """
        loc_matrix = glGetUniformLocation(program, "mat_transformation")

        # Apply the camera movements after the cubie movements to preserve the cubie coordinates
        result_mat = self.camera @ self.camera_rotation @ self.mat
        glUniformMatrix4fv(loc_matrix, 1, GL_TRUE, result_mat.reshape(16))

        for i in range(6):
            self.drawFace(program, vert_start_idx, i)
