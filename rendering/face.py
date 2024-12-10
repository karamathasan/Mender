from rendering.edge import Edge2D, Edge3D
from rendering.quaternion import Quaternion
import numpy as np
import pygame
from camera import Camera3D

class Face():

    '''
    Create a 3D face for rendering

    Parameters:
        points: a list of points in 3D space that form the triangular face. the points must be in counterclockwise order relative to the normal of the face
    '''
    def __init__(self, *args: np.ndarray):
        for point in args:
            assert point.shape == (3,) 
        self.a, self.b, self.c = args

class Triangle(Face):
    def __init__(self, *args, color: str = "white"):
        super().__init__(*args)
        self.normal = np.cross((self.c - self.a), (self.b - self.a))
        self.normal = self.normal / np.linalg.norm(self.normal)
    
    def draw(self, camera: Camera3D):
        # needs to account for rotations. 
        a = camera.Vec2Screen(self.a)
        b = camera.Vec2Screen(self.b)
        c = camera.Vec2Screen(self.c)
        
        color = np.dot(camera.getGlobalDirection(),self.normal)

        pygame.draw.polygon(surface=camera.screen, color="white", points=[a, b, c])

    @staticmethod
    def fromQuad(*points: np.ndarray):
        for point in points:
            assert point.shape == (3,) 
        a,b,c,d = points
        return Triangle(a,b,c), Triangle(c,d,a)
# class Quad():
#     pass